from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductVariantSerializer

class AddToCartSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)

class CartItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'variant', 'quantity', 'price', 'sub_total')

    def get_sub_total(self, obj):
        return obj.quantity * obj.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_price', 'updated_at')

    def get_total_price(self, obj):
        return sum(item.quantity * item.price for item in obj.items.all())