# carts/serializers.py

from rest_framework import serializers
from .models import Cart, CartItem
from products.models import ProductOptionValue, ProductVariant
from products.serializers import ProductVariantSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    option_values = serializers.PrimaryKeyRelatedField(queryset=ProductOptionValue.objects.all(), many=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'quantity', 'option_values', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'expires_at', 'items', 'get_total']
