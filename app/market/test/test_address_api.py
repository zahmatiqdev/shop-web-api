from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Address

from market.serializers import AddressSerializer


ADDRESS_URL = reverse('market:address')


class PublicAddressApiTests(TestCase):
    """Test the publicly available address API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving address"""
        res = self.client.get(ADDRESS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAddressApiTests(TestCase):
    """Test the authorized user address API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'abcd123123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_addresses(self):
        """Test retrieving addresses"""
        Address.objects.create(
            user=self.user,
            address='40. Adibstreet, Mashhad, Iran'
        )
        Address.objects.create(
            user=self.user,
            address='20. Shariati, Teheran, Iran'
        )

        res = self.client.get(ADDRESS_URL)

        addresses = Address.objects.all().order_by('-address')
        serializer = AddressSerializer(addresses, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_address_invalid(self):
        """Test creating a new address with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(ADDRESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
