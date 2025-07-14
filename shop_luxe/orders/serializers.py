from rest_framework import serializers
from .models import Order, OrderItem, Payment
from accounts.serializers import UserProfileSerializer
from products.models import ProductVariant

class ProductVariantDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ProductVariant
        fields = ('id', 'product_name', 'attributes')

class OrderItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantDetailSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'variant', 'quantity', 'price')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'amount', 'status', 'gateway', 'transaction_id', 'created_at')

class OrderListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_amount', 'status', 'payment_status', 'ordered_at')

class OrderDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_amount', 'status', 'shipping_address',
            'payment_method', 'payment_status', 'ordered_at', 'notes',
            'items',
            'payments'
        ]