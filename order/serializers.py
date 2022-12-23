from rest_framework import serializers
from .models import Product, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'quantity')


class OrderProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

        # fields = ("id", "quantity")


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', "status", 'date_placed', "products")
        read_only_fields = ('id', 'customer', 'date_placed', "status")

    @staticmethod
    def convert_products_to_id_list(data):
        """
        :param data:
        :type data:
        :return:
        :rtype:
        """

        id_list = [product_dict['id'] for product_dict in data]
        return id_list

    def validate_products(self, data):
        sorted_product_data = list(sorted(data, key=lambda i: i['id']))

        id_list = self.convert_products_to_id_list(sorted_product_data)
        if len(id_list) != len(set(id_list)):
            raise serializers.ValidationError("duplicate input product id")

        product_qs = Product.objects.filter(id__in=id_list).order_by("id").values("id", "quantity")

        # check if any product from input is not there &&  check if quantity is less and return error
        product_err_msgs = []
        for indx, product_dict in enumerate(sorted_product_data):

            available_quantity = product_qs[indx]["quantity"]

            if product_dict["quantity"] > available_quantity:
                err_msg = {product_dict["id"]: f"only {available_quantity} item available"}
                product_err_msgs.append(err_msg)

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