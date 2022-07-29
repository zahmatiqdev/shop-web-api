from datetime import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Order, Address

from market.serializers import OrderSerializerCreate, \
    OrderSerializerList, OrderSerializerDetail


ORDER_CREATE_URL = reverse('market:order-create')
ORDER_LIST_URL = reverse('market:order-list')


def detail_url(order_id):
    """Return Order detail URL"""
    return reverse('market:order-detail', args=[order_id])


def sample_address(user, name='Address sample'):
    """Create and return a sample address"""
    return Address.objects.create(user=user, name=name)


def sample_order(user, address, **params):
    """Create and return a sample order"""
    defaults = {
        'note': 'Sample Note',
        'delivery': datetime.now(),
    }
    defaults.update(params)

    return Order.objects.create(user=user, address=address, **defaults)


class PublicOrderApiTests(TestCase):
    """Test the publicly available order API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving order"""
        res = self.client.get(ORDER_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderApiTests(TestCase):
    """Test the authorized user order API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'abcd123123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_order_invalid(self):
        """Test creating a new order with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(ORDER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_order(self):
        """Test retrieving a list of recipes"""
        address_1 = sample_address(self.user, name='Tehran, Iran')
        address_2 = sample_address(self.user, name='Maschhad, Iran')
        sample_order(user=self.user, address=address_1)
        sample_order(user=self.user, address=address_2)

        res = self.client.get(ORDER_LIST_URL)

        orders = Order.objects.all().order_by('-delivery')
        serializer = OrderSerializerList(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
