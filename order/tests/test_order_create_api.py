from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from order.models import Product, Order

User = get_user_model()


class OrderCreateAPIViewTestCase(APITestCase):


    def setUp(self):
        self.client = APIClient()
        self.url = "/api/orders"
        # create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

        # create some test products
        self.product1 = Product.objects.create(id=1, name='Product 1', price=10, quantity=10)
        self.product2 = Product.objects.create(id=2, name='Product 2', price=20, quantity=5)

        self.valid_product_data = [
            {'id': self.product1.id, 'quantity': 5, "price":1},
            {'id': self.product2.id, 'quantity': 3, "price":1},
        ]

        self.invalid_product_data = [
            {'id': self.product1.id, 'quantity': 15}, # quantity is more than available
            {'id': self.product2.id, 'quantity': 3},
        ]
        self.duplicate_product_data = [
            {'id': self.product1.id, 'quantity': 5},
            {'id': self.product2.id, 'quantity': 3},
            {'id': self.product1.id, 'quantity': 5},
        ]
        self.invalid_product_id_data = [
            {'id': 100, 'quantity': 5}, # product with this id does not exist
            {'id': self.product2.id, 'quantity': 3},
        ]

    def test_create_order(self):
        # log in the test user
        self.client.force_authenticate(user=self.user)
        # send a POST request to the create order endpoint with the valid product data
        response = self.client.post(path=self.url,  data={"products": self.valid_product_data}, format="json")
        self.assertEqual(response.status_code, 201)  # HTTP 201 Created

        # check if the order was created and the order items were created correctly
        order = Order.objects.first()
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.status, Order.PENDING)
        self.assertEqual(order.orderitem_set.count(), 2)
        self.assertEqual(order.orderitem_set.get(product=self.product1).quantity, 5)
        self.assertEqual(order.orderitem_set.get(product=self.product2).quantity, 3)

        # check if the quantity of the products was updated correctly
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.quantity, 5)
        self.product2.refresh_from_db()
        self.assertEqual(self.product2.quantity, 2)

    def test_create_order_with_invalid_product_id(self):
        # Send the request to the API endpoint
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.url,
            data={"products": self.invalid_product_id_data},
            format="json"
        )

        # Verify the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {'products': {'100': 'product with id 100 does not exist'}}
        )

    def test_duplicate_product_data_cause_400(self):
        # Send a request with self.duplicate_product_data as payload
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, json={"products": self.duplicate_product_data})

        # Verify that the response has a 400 Bad Request status code
        self.assertEqual(response.status_code, 400)
