# services/order_service.py

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from decimal import Decimal
from products.models import Product, ProductVariant
from order.models import Order, OrderItem
from user.models import User
from typing import List, Dict, Optional
import uuid


class OrderService:
    """
    Service Layer for Order Operations.
    Handles business logic, validation, and database operations 
    for creating, updating, and managing orders.
    """

    @staticmethod
    @transaction.atomic
    def create_order(user: User, items: List[Dict], shipping_address: str, coupon: Optional[Dict] = None) -> Order:
        """
        Create a new Order with associated items.

        Args:
            user (User): The user who is placing the order.
            items (List[Dict]): List of items to purchase.
            shipping_address (str): The shipping address for the order.
            coupon (Dict, optional): Coupon data if available.

        Returns:
            Order: The created order instance.
        """
        order = Order.objects.create(
            id=uuid.uuid4(),
            user=user,
            total_price=Decimal('0.00'),
            shipping_address=shipping_address,
            created_at=now(),
            is_paid=False,
            status='Pending'
        )

        total_price = Decimal('0.00')

        for item_data in items:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity', 1)
            variant_id = item_data.get('variant_id')

            # 🔹 Retrieve Product and Optional Variant
            product = Product.objects.select_for_update().get(id=product_id)
            if variant_id:
                variant = ProductVariant.objects.get(id=variant_id)
                price = variant.additional_price + product.price
            else:
                price = product.price

            # 🔹 Update stock
            if product.stock_quantity < quantity:
                raise ValueError(f"Not enough stock for product {product.name}. Available: {product.stock_quantity}")

            product.stock_quantity -= quantity
            product.save()

            # 🔹 Create OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                variant=variant if variant_id else None,
                quantity=quantity,
                price=price
            )

            total_price += price * quantity

        # 🔹 Apply coupon if available
        if coupon:
            discount_amount = coupon.get('discount_amount', Decimal('0.00'))
            discount_percentage = coupon.get('discount_percentage', 0)
            if discount_percentage > 0:
                total_price -= (total_price * Decimal(discount_percentage / 100))
            total_price -= discount_amount

        # 🔹 Update final price
        order.total_price = max(total_price, Decimal('0.00'))
        order.save()

        return order

    @staticmethod
    def get_order_details(order_id: str) -> Optional[Order]:
        """
        Retrieve order details, including items.

        Args:
            order_id (str): The UUID of the order.

        Returns:
            Optional[Order]: The order instance if found, else None.
        """
        try:
            return Order.objects.prefetch_related('items__product', 'items__variant').get(id=order_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_orders(user: User) -> List[Order]:
        """
        Retrieve all orders for a specific user.

        Args:
            user (User): The user whose orders are to be retrieved.

        Returns:
            List[Order]: List of orders for the user.
        """
        return list(Order.objects.filter(user=user).prefetch_related('items__product', 'items__variant'))

    @staticmethod
    @transaction.atomic
    def update_order_status(order_id: str, status: str) -> bool:
        """
        Update the status of an order.

        Args:
            order_id (str): The UUID of the order.
            status (str): The new status to update.

        Returns:
            bool: True if updated successfully, False if not found.
        """
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    @transaction.atomic
    def cancel_order(order_id: str) -> bool:
        """
        Cancel an order and restore product stock.

        Args:
            order_id (str): The UUID of the order.

        Returns:
            bool: True if canceled successfully, False if not found.
        """
        try:
            order = Order.objects.select_for_update().get(id=order_id)
            if order.status != 'Cancelled':
                order.status = 'Cancelled'
                order.save()

                # 🔹 Restore stock
                for item in order.items.all():
                    item.product.stock_quantity += item.quantity
                    item.product.save()
                return True
            return False
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def calculate_order_total(order: Order) -> Decimal:
        """
        Calculate the total cost of an order.

        Args:
            order (Order): The order instance.

        Returns:
            Decimal: The calculated total price.
        """
        total = sum(item.price * item.quantity for item in order.items.all())
        return total

