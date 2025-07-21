from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import views, status
from rest_framework.response import Response
from django.db.models import Q
from accounts.permissions import IsSellerUser
from .serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer, ProductSearchSerializer, CategorySearchSerializer, ProductCreateSerializer
from .models import Product, Category
from django.core.cache import cache


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'product_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=3600)
        return response


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_available=True)
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        cache_key = f'product_detail_{pk}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=3600) 
        return response


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'category_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=86400)
        return response


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        cache_key = f'category_detail_{pk}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=86400)
        return response


class GlobalSearchView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)

        if not query:
            return Response(
                {"error": "A search query ('q' parameter) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        product_results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            is_available=True
        )

        category_results = Category.objects.filter(name__icontains=query)

        product_serializer = ProductSearchSerializer(product_results, many=True)
        category_serializer = CategorySearchSerializer(category_results, many=True)

        data = {
            'products': product_serializer.data,
            'categories': category_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)
    
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAuthenticated, IsSellerUser]