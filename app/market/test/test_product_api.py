from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from market.serializers import ProductSerializer


PRODUCT_URL = reverse('market:product')


class PublicProductApiTests(TestCase):
    """Test the publicly available product API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving product"""
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTests(TestCase):
    """Test the authorized user product API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'abcd123123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving products"""
        Product.objects.create(name='banana')
        Product.objects.create(name='apple')

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.all().order_by('-name')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_product_invalid(self):
        """Test creating a new product with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
