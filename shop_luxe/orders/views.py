from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import OrderListSerializer, OrderItemSerializer
from .models import Order, OrderItem

class OrderListView(generics.ListAPIViews):
    pass