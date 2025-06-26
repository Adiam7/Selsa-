from rest_framework import serializers
from .models import (
    Product,
    ProductImage,
    ProductOptionType,
    ProductOptionValue,
    ProductVariant #,
    #FieldType
)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class ProductOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionValue
        fields = "__all__"

class ProductOptionTypeSerializer(serializers.ModelSerializer):
    values = ProductOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOptionType
        fields = ["id", "name", "field_type", "values"]

class ProductVariantSerializer(serializers.ModelSerializer):
    option_values = ProductOptionValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.Serializer):
    product_slug = serializers.CharField(max_length=255)
    option_values = serializers.DictField(child=serializers.CharField())
    quantity = serializers.IntegerField(min_value=1)
