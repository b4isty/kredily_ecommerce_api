from django.urls import path
from .views import ProductListAPIView, OrderCreateAPIView, OrderListAPIView
app_name = "order"


urlpatterns = [
    path("products", ProductListAPIView.as_view(), name="product_list"),
    path('orders', OrderCreateAPIView.as_view(), name="create"),
    path('orders-history', OrderListAPIView.as_view(), name="order_history")
]
