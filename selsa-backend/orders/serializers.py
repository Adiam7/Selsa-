# orders/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem, Payment
from products.serializers import ProductVariantSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'quantity', 'price', 'get_total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_amount', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        # Calculate total
        order.calculate_total()
        return order


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'stripe_payment_intent', 'amount', 'status', 'created_at']
        read_only_fields = ['created_at', 'stripe_payment_intent', 'amount', 'status']