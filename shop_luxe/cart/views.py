from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import ProductVariant
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)

class CartDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        variant_id = serializer.validated_data['variant_id']
        quantity = serializer.validated_data['quantity']
        
        variant = get_object_or_404(ProductVariant, id=variant_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        try:
            cart_item = cart.items.get(variant=variant)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                variant=variant,
                quantity=quantity,
                price=variant.price 
            )

        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)

class UpdateCartItemView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class RemoveFromCartView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)