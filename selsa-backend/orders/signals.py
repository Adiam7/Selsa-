# orders/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order,OrderItem
from products.models import ProductVariant

# ✅ 1️⃣ Stock Deduction when Order is Placed
@receiver(post_save, sender=OrderItem)
def decrease_stock_on_order(sender, instance, created, **kwargs):
    """
    Deduct stock when an OrderItem is created.
    """
    if created:
        variant = instance.product_variant
        if variant.stock_control == "finite":
            if variant.stock_quantity >= instance.quantity:
                variant.stock_quantity -= instance.quantity
                variant.save()
                print(f"✅ Stock updated for {variant}: {variant.stock_quantity} remaining.")
            else:
                raise ValueError("Not enough stock available for this variant.")

# ✅ 2️⃣ Stock Restoration when Order is Canceled or Refunded
@receiver(post_save, sender=Order)
def restore_stock_on_cancel_or_refund(sender, instance, **kwargs):
    """
    Restore stock if an order is canceled or refunded.
    """
    if instance.status in ['canceled', 'refunded']:
        for item in instance.items.all():
            variant = item.product_variant
            if variant.stock_control == "finite":
                variant.stock_quantity += item.quantity
                variant.save()
                print(f"🔄 Stock restored for {variant}: {variant.stock_quantity} remaining.")

# ✅ 3️⃣ Stock Adjustment when OrderItem is Deleted
@receiver(post_delete, sender=OrderItem)
def restore_stock_on_item_delete(sender, instance, **kwargs):
    """
    Restore stock when an OrderItem is deleted (e.g., removed from order).
    """
    variant = instance.product_variant
    if variant.stock_control == "finite":
        variant.stock_quantity += instance.quantity
        variant.save()
        print(f"🔄 Stock restored for {variant}: {variant.stock_quantity} remaining.")

# @receiver(post_save, sender=OrderItem)
# def update_stock_on_order(sender, instance, created, **kwargs):
#     """
#     🔄 Decrease stock when an order is confirmed.
#     """
#     if created and instance.product_variant.stock_control == "finite":
#         instance.product_variant.stock_quantity = max(0, instance.product_variant.stock_quantity - instance.quantity)
#         instance.product_variant.save()
#         print(f"✅ Stock updated for {instance.product_variant}: {instance.product_variant.stock_quantity} remaining.")

# @receiver(post_delete, sender=OrderItem)
# def restore_stock_on_order_cancel(sender, instance, **kwargs):
#     """
#     🔄 Restore stock when an order is canceled.
#     """
#     if instance.product_variant.stock_control == "finite":
#         instance.product_variant.stock_quantity += instance.quantity
#         instance.product_variant.save()
#         print(f"🔄 Stock restored for {instance.product_variant}: {instance.product_variant.stock_quantity} remaining.")

