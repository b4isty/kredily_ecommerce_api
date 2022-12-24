from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, OrderListSerializer


# Create your views here.

class ProductListAPIView(ListAPIView):
    """Product List View"""
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("id")


class OrderListCreateAPIView(ListCreateAPIView):
    """ListCreate Order View"""

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user
        ).prefetch_related("orderitem_set").order_by('-date_placed')


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        elif self.request.method == 'POST':
            return OrderSerializer
