from django.urls import path
from .views import ProductListAPIView, OrderListCreateAPIView
app_name = "order"


urlpatterns = [
    path("products", ProductListAPIView.as_view(), name="product_list"),
    path('orders', OrderListCreateAPIView.as_view(), name="order_list_create"),
]
