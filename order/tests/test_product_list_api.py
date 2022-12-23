from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from order.models import Product


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
        self.url = "/api/products"

    def test_pagination(self):
        # Set up test data
        Product.objects.create(name='Product 1', price=10.00, quantity=5)
        Product.objects.create(name='Product 2', price=20.00, quantity=10)
        Product.objects.create(name='Product 3', price=30.00, quantity=15)
        Product.objects.create(name='Product 4', price=40.00, quantity=20)
        Product.objects.create(name='Product 5', price=50.00, quantity=25)

        # Send request to product list endpoint with page parameter
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)

        # Assert that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the correct number of products was returned
        self.assertEqual(len(response.data["results"]), 5)

        # Assert that the list includes the correct product details
        self.assertEqual(response.data["results"][0]['id'], 1)
        self.assertEqual(response.data["results"][0]['name'], 'Product 1')
        self.assertEqual(float(response.data["results"][0]['price']), 10.00)
        self.assertEqual(response.data["results"][0]['quantity'], 5)

    def test_unauthenticated_request(self):
        # Send request to product list endpoint without authentication
        response = self.client.get(self.url)

        # Assert that the request was denied with a 401 Unauthorized status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

