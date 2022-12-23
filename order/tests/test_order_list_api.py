from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from order.models import Product, Order


class ProductListAPITestCase(APITestCase):
    """
    ProductListAPITestCase test the product list api code
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test_admin",
            email="test_admin@example.com"
        )


    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/orders"

    def test_only_returns_authenticated_user_orders(self):
        # Create a user and an order belonging to that user
        Order.objects.create(customer=self.user)

        # Create another user and an order belonging to that user
        other_user = get_user_model().objects.create_user(username='otheruser', password='otherpass')
        other_order = Order.objects.create(customer=other_user)

        # Log in as the first user
        self.client.force_authenticate(other_user)

        # Send a GET request to the view
        response = self.client.get(self.url)

        self.assertEqual(response.data["results"][0]["id"], other_order.id)
