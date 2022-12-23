from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    """Product Serializer"""
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity')


class OrderProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)



class OrderSerializer(serializers.ModelSerializer):
    """Order Create Serializer"""
    products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', "status", 'date_placed', "products")
        read_only_fields = ('id', 'customer', 'date_placed', "status")

    @staticmethod
    def convert_products_to_id_list(data):
        """
        Convert product data dictionaries to list of product ids
        """

        id_list = [product_dict['id'] for product_dict in data]
        return id_list

    def validate_products(self, data):
        sorted_product_data = list(sorted(data, key=lambda i: i['id']))

        id_list = self.convert_products_to_id_list(sorted_product_data)
        if len(id_list) != len(set(id_list)):
            raise serializers.ValidationError("duplicate input product id")

        product_qs = Product.objects.filter(id__in=id_list).order_by("id").values("id", "quantity")
        product_quantities = {p["id"]: p["quantity"] for p in product_qs}

        product_err_msgs = {}
        for product_dict in sorted_product_data:
            product_id = product_dict["id"]
            if product_id not in product_quantities:
                err_msg = f"product with id {product_id} does not exist"
                product_err_msgs[product_id] = err_msg
            elif product_dict["quantity"] > product_quantities[product_id]:
                err_msg = f"only {product_quantities[product_id]} items available"
                product_err_msgs[product_id] = err_msg

        if product_err_msgs:
            raise serializers.ValidationError(product_err_msgs)
        return data


    def create(self, validated_data):
        products = validated_data.pop("products")

        order_obj = Order.objects.create(
            status = Order.PENDING,
            customer= self.context['request'].user
        )
        # re-calculate quantity
        product_qs = Product.objects.filter(id__in=self.convert_products_to_id_list(data=products))

        # Create a dictionary that maps id to the corresponding updated quantity
        product_updates = {product['id']: product['quantity'] for product in products}
        for product_obj in product_qs:
            product_obj.quantity -= product_updates[product_obj.id]
            product_obj.save(update_fields=["quantity"])

        order_item_list = []
        for product_data in products:
            order_item_obj = OrderItem(
                order=order_obj,
                quantity=product_data["quantity"],
                product_id=product_data["id"],
            )
            order_item_list.append(order_item_obj)

        OrderItem.objects.bulk_create(order_item_list)
        return order_obj

class OrderItemSerializer(serializers.ModelSerializer):
    """Order Item Serializer"""
    class Meta:
        model = OrderItem
        fields = ("product", "quantity")

class OrderListSerializer(serializers.ModelSerializer):
    """Order History List Serializer"""
    order_items = serializers.SerializerMethodField("_get_order_items", required=False, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "customer", "status", "date_placed", "order_items")
    def _get_order_items(self, order):
        serializer = OrderItemSerializer(order.orderitem_set.all(), many=True, read_only=True)
        return serializer.data
