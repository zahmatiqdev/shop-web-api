from rest_framework import generics, mixins, authentication, permissions

from core.models import Product, Unit, Address, Order, OrderItem
from market.serializers import ProductSerializer, UnitSerializer, AddressSerializer, \
    OrderSerializerCreate, OrderSerializerList, OrderSerializerDetail, OrderItemSerializer, FullOrderSerializerCreate



class ProductAPIView(generics.CreateAPIView, generics.ListAPIView):
    """ Define Product View for Create & List"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class UnitAPIView(generics.CreateAPIView, generics.ListAPIView):
    """ Define Unit View for Create & List"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()


class AddressAPIView(generics.CreateAPIView, generics.ListAPIView):
    """ Define Address View for Create & List"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderCreateAPIView(generics.CreateAPIView):
    """Define Order View only for Create"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderSerializerCreate
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderListAPIView(generics.ListAPIView):
    """Define Order View only for List"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderSerializerList
    queryset = Order.objects.all()


class OrderDetailAPIView(generics.RetrieveAPIView):
    """Define Order View only for Detail"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderSerializerDetail
    queryset = Order.objects.all()


class OrderItemCreateAPIView(generics.CreateAPIView):
    """Define OrderItem View only for Create"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FullOrderCreateAPIView(generics.CreateAPIView):
    """Define Order View only for Create"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FullOrderSerializerCreate
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
