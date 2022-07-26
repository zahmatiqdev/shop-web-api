from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Unit

from market.serializers import UnitSerializer


UNIT_URL = reverse('market:unit')


class PublicUnitApiTests(TestCase):
    """Test the publicly available unit API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving unit"""
        res = self.client.get(UNIT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUnitApiTests(TestCase):
    """Test the authorized user unit API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'abcd123123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_units(self):
        """Test retrieving units"""
        Unit.objects.create(name='kg')
        Unit.objects.create(name='gram')

        res = self.client.get(UNIT_URL)

        units = Unit.objects.all().order_by('-name')
        serializer = UnitSerializer(units, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_unit_invalid(self):
        """Test creating a new unit with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(UNIT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
