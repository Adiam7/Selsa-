# # order/signals.py

# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import OrderItem
# from products.models import ProductVariant

# @receiver(post_save, sender=OrderItem)
# def update_stock_on_order(sender, instance, created, **kwargs):
#     if created:
#         variant = instance.product_variant
#         if variant.stock_control == "finite":
#             variant.stock_quantity = max(0, variant.stock_quantity - instance.quantity)
#             variant.save()


# @receiver(post_delete, sender=OrderItem)
# def restore_stock_on_order_cancel(sender, instance, **kwargs):
#     variant = instance.product_variant
#     if variant.stock_control == "finite":
#         variant.stock_quantity += instance.quantity
#         variant.save()
