from rest_framework import serializers
from .models import Review
from accounts.serializers import UserProfileSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'product', 'rating', 'comment', 'created_at')