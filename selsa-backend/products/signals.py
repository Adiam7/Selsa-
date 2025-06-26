# products/signals.py
# from django.db.models.signals import m2m_changed
# from django.db import transaction
# from django.dispatch import receiver
# from .models import ProductVariant

# @receiver(m2m_changed, sender=ProductVariant.option_values.through)
# def generate_option_combination_and_sku(sender, instance, action, **kwargs):
#     """
#     Handles the SKU and option combination generation after M2M relationship is committed.
#     """
#     if action == "post_add":
#         with transaction.atomic():
#             # 🔄 Refresh the ManyToMany field
#             instance.refresh_from_db()

#             # ✅ Generate Option Combination
#             option_ids = list(instance.option_values.values_list('id', flat=True))
#             if option_ids:
#                 instance.option_combination = '-'.join(map(str, sorted(option_ids)))

#                 # ✅ Check for uniqueness WITHIN the product
#                 existing_variant = ProductVariant.objects.filter(
#                     product=instance.product,
#                     option_combination=instance.option_combination
#                 ).exclude(pk=instance.pk).first()

#                 if existing_variant:
#                     raise ValueError(
#                         f"A variant with this option combination already exists for this product: {existing_variant.sku}"
#                     )

#                 # ✅ Generate SKU if not already set
#                 if not instance.sku:
#                     option_values = instance.option_values.select_related('option_type').all()
#                     option_parts = [
#                         f"{v.option_type.name[:3].upper()}-{v.value[:3].upper()}"
#                         for v in option_values
#                     ]
#                     option_code = "-".join(option_parts)
#                     instance.sku = f"{instance.product.slug}-{option_code}-{instance.pk}"

#                 # ✅ Save within the atomic block
#                 instance.save(update_fields=['option_combination', 'sku'])


# products/signals.py

import hashlib
from django.db.models.signals import m2m_changed
from django.db import transaction
from django.dispatch import receiver
from .models import ProductVariant, ProductOptionValue

def generate_unique_sku(product_slug, option_ids):
    """
    Generates a unique SKU for a ProductVariant.
    """
    # 🔄 Sort and join the option values for consistency
    option_combination = '-'.join(map(str, sorted(option_ids)))

    # 🧮 Hash the combination to ensure uniqueness
    hash_object = hashlib.md5(option_combination.encode())
    unique_hash = hash_object.hexdigest()[:5].upper()

    # 🏷️ Final SKU
    return f"{product_slug}-{option_combination}-{unique_hash}"

@receiver(m2m_changed, sender=ProductVariant.option_values.through)
def generate_sku_and_combination(sender, instance, action, **kwargs):
    """
    Handles SKU and option combination generation after M2M relationship is committed.
    """
    if action == "post_add":
        with transaction.atomic():
            instance.refresh_from_db()
            option_ids = list(instance.option_values.values_list('id', flat=True))

            if option_ids:
                # ✅ Generate SKU and Combination
                instance.option_combination = '-'.join(map(str, sorted(option_ids)))
                instance.sku = generate_unique_sku(instance.product.slug, option_ids)
                
                # ✅ Check for uniqueness WITHIN the product
                existing_variant = ProductVariant.objects.filter(
                    product=instance.product,
                    option_combination=instance.option_combination
                ).exclude(pk=instance.pk).first()

                if existing_variant:
                    raise ValueError(
                        f"A variant with this option combination already exists for this product: {existing_variant.sku}"
                    )

                # ✅ Save
                instance.save(update_fields=['option_combination', 'sku'])

# products/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductVariant
from orders.models import OrderItem  

@receiver(post_save, sender=OrderItem)
def update_stock_on_order(sender, instance, created, **kwargs):
    """
    🔄 Decrease stock when an order is confirmed.
    This logic belongs to the product, as it is directly modifying product state.
    """
    if created:
        variant = instance.product_variant
        if variant.stock_control == "finite":
            # Decrease the stock quantity
            variant.stock_quantity = max(0, variant.stock_quantity - instance.quantity)
            variant.save()
            print(f"✅ Stock updated for {variant}: {variant.stock_quantity} remaining.")

@receiver(post_delete, sender=OrderItem)
def restore_stock_on_order_cancel(sender, instance, **kwargs):
    """
    🔄 Restore stock when an order is canceled.
    This logic belongs to the product, as it is directly modifying product state.
    """
    variant = instance.product_variant
    if variant.stock_control == "finite":
        # Restore the stock quantity
        variant.stock_quantity += instance.quantity
        variant.save()
        print(f"🔄 Stock restored for {variant}: {variant.stock_quantity} remaining.")
