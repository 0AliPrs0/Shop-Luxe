from rest_framework import serializers
from .models import Category, Product, ProductVariant, ProductImage
from django.db import transaction

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'price', 'stock', 'attributes')
        read_only_fields = ('id',)

class ProductCreateSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ('category', 'name', 'slug', 'description', 'specifications', 'images', 'variants')

    def create(self, validated_data):
        with transaction.atomic():
            variants_data = validated_data.pop('variants')
            
            product = Product.objects.create(**validated_data)
            
            for variant_data in variants_data:
                ProductVariant.objects.create(product=product, **variant_data)
                
        return product

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

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product')
        read_only_fields = ('product',)