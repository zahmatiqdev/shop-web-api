from rest_framework import serializers

from core.models import Product, Unit, Address, Order, OrderItem
from user.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product object"""

    class Meta:
        model = Product
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit object"""

    class Meta:
        model = Unit
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address object"""

    class Meta:
        model = Address
        fields = ('name',)
        read_only_field = ('user', 'id',)


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem object"""

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'unit', 'quantity']


class OrderItemCustomSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem object & display the details of the items
    that we use for the OrderSerializerDetail method"""
    product = ProductSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'unit', 'quantity']


class OrderSerializerCreate(serializers.ModelSerializer):
    """Serializer for Order object"""

    class Meta:
        model = Order
        fields = ['delivery', 'note', 'address']
        read_only_field = ('user',)


class OrderSerializerList(serializers.ModelSerializer):
    """Serializer for Order object & display user information and address"""
    address = AddressSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery', 'note', 'address']


class OrderSerializerDetail(serializers.ModelSerializer):
    """Serializer for Order object & display item details,
    user information and address"""
    # user = UserSerializer(read_only=True)
    # address = AddressSerializer(read_only=True)
    products = OrderItemCustomSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery', 'note', 'address', 'products']


class FullOrderItemSerializer(serializers.ModelSerializer):
    """FullOrderItemSerializer for OrderItem object."""

    class Meta:
        model = OrderItem
        fields = ['product', 'unit', 'quantity']


class FullOrderSerializerCreate(serializers.ModelSerializer):
    """Serializer for Order object"""
    products = FullOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['delivery', 'note', 'address', 'products']
        read_only_field = ('user', 'id',)

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            OrderItem.objects.create(order=order, **product_data)
        return order
