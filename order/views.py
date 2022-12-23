from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, OrderListSerializer


# Create your views here.

class ProductListAPIView(ListAPIView):
    """Product List View"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("id")


class OrderCreateAPIView(CreateAPIView):
    """Create Order View"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class OrderListAPIView(ListAPIView):
    """Order History View"""
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderListSerializer

    def get_queryset(self):
        orders = Order.objects.filter(
            customer=self.request.user
        ).prefetch_related("orderitem_set").order_by("-date_placed")
        return orders
