from rest_framework import serializers
from .models import Category
from products.models import Product  # import as needed

class ProductSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price']  # Add more if needed

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'parent',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
