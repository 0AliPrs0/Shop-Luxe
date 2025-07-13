from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import ReviewSerializer
from .models import Review
from products.models import Product

class ReviewListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        serializer.save(user=self.request.user, product=product)

