from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ProductListSerializer, ProductDetailSerializer
from .models import Product

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailSerializer


    
