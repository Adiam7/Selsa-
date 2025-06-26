# carts/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from products.models import ProductVariant
from .models import Cart,CartItem
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from orders.models import Payment, Order


@receiver(post_save, sender=ProductVariant)
def auto_remove_out_of_stock_items(sender, instance, **kwargs):
    """
    Automatically removes items from all carts if the product's stock is 0.
    """
    if instance.stock_control == "finite" and instance.stock_quantity <= 0:
        # Find all CartItems with this ProductVariant
        cart_items = CartItem.objects.filter(product_variant=instance)
        if cart_items.exists():
            print(f"🛑 Removing {cart_items.count()} items from carts (Out of Stock)")
            cart_items.delete()


@receiver(pre_save, sender=ProductVariant)
def sync_cart_items_with_stock(sender, instance, **kwargs):
    """
    Synchronizes the quantity of cart items with available stock.
    """
    if instance.stock_control == "finite":
        # Get all CartItems with this ProductVariant
        cart_items = CartItem.objects.filter(product_variant=instance)
        
        for cart_item in cart_items:
            if cart_item.quantity > instance.stock_quantity:
                print(f"⚠️ Reducing quantity in Cart (ID: {cart_item.cart.id}) for {cart_item.product_variant}")
                cart_item.quantity = instance.stock_quantity
                cart_item.save()


@receiver(post_save, sender=Cart)
def check_cart_expiration(sender, instance, **kwargs):
    """ Automatically expire the cart if the expiration time is reached. """
    if instance.status == 'open' and instance.expires_at and instance.is_expired():
        with transaction.atomic():
            print(f"🕒 Cart {instance.id} has expired.")
            instance.expire()


@receiver(post_save, sender=Cart)
def handle_payment_status(sender, instance, **kwargs):
    """
    Handles stock finalization or restoration based on payment status.
    """
    if instance.status == 'payment_failed':
        print(f"❌ Payment failed for Cart {instance.id}. Restoring stock.")
        instance.cancel_checkout()

    elif instance.status == 'checked_out':
        print(f"💰 Payment completed for Cart {instance.id}. Stock finalized.")


@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):
    if instance.status == 'succeeded':
        instance.order.status = 'completed'
        instance.order.save()
    elif instance.status == 'failed':
        instance.order.status = 'canceled'
        instance.order.save()
