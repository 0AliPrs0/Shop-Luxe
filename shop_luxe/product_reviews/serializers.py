from rest_framework import serializers
from .models import Review
from accounts.serializers import UserProfileSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'rating', 'comment', 'created_at')
        read_only_fields = ('product_id',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['product_id'] = self.context['view'].kwargs['product_id']
        return super().create(validated_data)