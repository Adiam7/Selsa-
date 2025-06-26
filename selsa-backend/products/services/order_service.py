# order_service.py

from products.models import Order, OrderItem, ProductVariant
from products.serializers import OrderSerializer
from django.db import transaction
from django.core.exceptions import ValidationError


class OrderService:
    
    @staticmethod
    @transaction.atomic
    def create_order(user, order_data):
        """
        Create a new order with order items.
        """
        items_data = order_data.pop('items', [])
        total_price = sum(item['price'] * item['quantity'] for item in items_data)
        order_data['user'] = user
        order_data['total_price'] = total_price
        
        order = Order.objects.create(**order_data)

        for item_data in items_data:
            variant_id = item_data.pop('variant_id')
            try:
                variant = ProductVariant.objects.get(id=variant_id)
                if variant.stock_quantity < item_data['quantity']:
                    raise ValidationError(f"Insufficient stock for {variant.product.name}")
                variant.stock_quantity -= item_data['quantity']
                variant.save()
                OrderItem.objects.create(order=order, product=variant.product, **item_data)
            except ProductVariant.DoesNotExist:
                raise ValidationError("Product Variant not found")

        return order

    @staticmethod
    def get_order(order_id):
        """
        Retrieve an order by its ID.
        """
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def get_user_orders(user):
        """
        Get all orders for a specific user.
        """
        return Order.objects.filter(user=user)

    @staticmethod
    def update_order_status(order_id, status):
        """
        Update the status of an order.
        """
        order = OrderService.get_order(order_id)
        if order:
            order.status = status
            order.save()
            return order
        return None
