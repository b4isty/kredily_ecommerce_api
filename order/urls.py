from django.urls import path
from .views import ProductListAPIView, OrderCreateAPIView, OrderListAPIView
app_name = "order"


urlpatterns = [
    path("products", ProductListAPIView.as_view()),
    path('orders', OrderCreateAPIView.as_view()),
    path('orders-history', OrderListAPIView.as_view())
]
