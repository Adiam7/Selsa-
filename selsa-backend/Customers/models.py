# apps/order/models.py

# from django.db import models
# from django.conf import settings
# from products.models import ProductVariant

# class Customer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, default='Pending')
#     is_paid = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"Order #{self.id} by {self.user.username}"


# class CustomerOrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, related_name="order_items")
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         unique_together = ('order', 'product_variant')

#     def __str__(self):
#         return f"{self.product_variant} (x{self.quantity})"