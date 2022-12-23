from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Product(models.Model):
    """
    A model representing a product that can be ordered by a customer.
    A product has a name, price, and quantity in stock.
    """
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    """
    A model representing an order placed by a customer.
    An order consists of multiple order items, each representing a product and its quantity.
    The order has a status indicating its current state in the fulfillment process.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, db_index=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_placed = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    """
    A model representing an item in an order.
    An order item consists of a product and a quantity, and belongs to a specific order.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
