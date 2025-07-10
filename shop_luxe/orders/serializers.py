from rest_framework import serializers
from .models import Order, OrderItem, Payment
from accounts.serializers import UserSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'quantity', 'price', 'variant']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'status', 'gateway', 'transaction_id', 'created_at']




class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'total_amount',
            'status',
            'payment_status',
            'ordered_at',
        ]