from rest_framework import serializers
from .models import Category, Product, ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'price', 'stock', 'attributes')

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'category', 'is_available')

class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'category', 'specifications', 'images', 'variants')

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'parent', 'image_url', 'children')

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data
    

class ProductSearchSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    variants = ProductVariantSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'category', 'variants')


class CategorySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')