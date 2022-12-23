from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Product
from .serializers import ProductSerializer
# Create your views here.

class ProductListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("id")
