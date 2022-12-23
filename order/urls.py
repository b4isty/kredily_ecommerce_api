from django.urls import path
from .views import ProductListAPIView, OrderCreateAPIView
app_name = "order"


urlpatterns = [
    path("products", ProductListAPIView.as_view()),
    path('orders', OrderCreateAPIView.as_view())
]
