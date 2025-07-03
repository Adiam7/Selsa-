# orders/models.py

from django.db import models
from django.conf import settings
from products.models import ProductVariant
from django.utils import timezone


class Order(models.Model):
    """ Represents a customer's order with status tracking. """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id} - User: {self.user} - Status: {self.status}"

    def calculate_total(self):
        """
        Calculate the total amount for the order and save it.
        """
        total = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])
        return total

    def add_item(self, variant, quantity):
        """
        Add an item to the order.
        - If the item already exists in the order, it increments the quantity.
        - Ensures there is enough stock before adding.
        """
        if variant.stock_control == "finite" and variant.stock_quantity < quantity:
            raise ValueError(f"Not enough stock for {variant.product.name} (Requested: {quantity}, Available: {variant.stock_quantity})")
        
        order_item, created = OrderItem.objects.get_or_create(order=self, product_variant=variant)
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        else:
            order_item.quantity = quantity
            order_item.price = variant.price
            order_item.save()

        self.calculate_total()
        return order_item

    def remove_item(self, variant):
        """
        Remove an item from the order.
        """
        try:
            order_item = OrderItem.objects.get(order=self, product_variant=variant)
            order_item.delete()
            self.calculate_total()
        except OrderItem.DoesNotExist:
            pass

    def clear_order(self):
        """ Clears all items from the order. """
        self.items.all().delete()
        self.calculate_total()

    def is_fully_paid(self):
        """ Check if the order is fully paid. """
        return self.status == 'completed'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, default=None)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('order', 'product_variant')
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.product_variant.product.name} ({self.product_variant.option_combination}) - Qty: {self.quantity}"

    def get_total_price(self):
        """Calculate the total price for this order item."""
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # ✅ Automatically set the price from the ProductVariant if not already set
        if not self.price:
            self.price = self.product_variant.price
        super().save(*args, **kwargs)
        
        # ✅ Recalculate the Order total
        if self.order:
            self.order.calculate_total()


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    stripe_payment_intent = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('succeeded', 'Succeeded'), ('failed', 'Failed')], default='failed')

    def __str__(self):
        return f"Payment for Order #{self.order.id} - Status: {self.status}"
