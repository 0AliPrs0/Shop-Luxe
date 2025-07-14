from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import views, status
from rest_framework.response import Response
from django.db.models import Q
from .serializers import ProductListSerializer, ProductDetailSerializer, CategorySerializer, ProductSearchSerializer, CategorySearchSerializer
from .models import Product, Category

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductListSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


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