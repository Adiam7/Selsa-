# carts/models.py

from django.db import models
from django.contrib.auth import get_user_model
from products.models import ProductVariant, ProductOptionValue, ProductImage
from django.utils import timezone
from django.core.exceptions import ValidationError
from orders.models import Order, OrderItem
from django.db import transaction
from django.contrib.auth.models import User
from datetime import timedelta


User = get_user_model()

class Cart(models.Model):
    """
    Represents a user's shopping cart. It can be associated with a user or remain session-based if the user is not logged in.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('checked_out', 'Checked Out'),
        ('expired', 'Expired'),
        ('pending_payment', 'Pending Payment'),
        ('payment_failed', 'Payment Failed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)  # For guest sessions
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)  

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        ordering = ['-created_at']

    def __str__(self):
        return f"Cart ({self.user or 'Session'}) - Status: {self.status}"

    def add_item(self, product_variant, quantity, option_values=None):
        """
        Adds or updates an item in the cart.
        """
        cart_item, created = CartItem.objects.get_or_create(
            cart=self, 
            product_variant=product_variant
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            if option_values:
                cart_item.option_values.set(option_values)  # Set option values if provided
            cart_item.quantity = quantity
            cart_item.save()

    def remove_item(self, cart_item):
        """
        Removes an item from the cart.
        """
        cart_item.delete()

    def clear(self):
        """
        Clears all items in the cart.
        """
        self.items.all().delete()

    def get_total(self):
        """
        Calculates the total price of all items in the cart.
        """
        return sum(item.get_total_price() for item in self.items.all())

    def checkout(self):
        """
        Transfers all items from the cart to an Order and validates stock levels.
        """
        """ Reserve stock and mark cart as pending payment """
        if self.status != 'open':
            raise ValueError("Cart is not in an open state")

        with transaction.atomic():
            for item in self.items.select_related('product_variant'):
                variant = item.product_variant
                if variant.stock_control == "finite" and variant.stock_quantity < item.quantity:
                    raise ValueError(f"Insufficient stock for {variant}")
                
                # Reserve stock
                variant.stock_quantity -= item.quantity
                variant.save()
            
            self.status = 'pending_payment'
            self.save()
            print(f"🛒 Cart {self.id} has been checked out. Stock reserved.")

        if not self.user:
            raise ValidationError("Checkout requires an authenticated user.")

        with transaction.atomic():
            # Create the Order
            order = Order.objects.create(user=self.user)
            
            for item in self.items.all():
                variant = item.product_variant
                
                # ⚠️ Validate Stock
                if variant.stock_control == "finite" and variant.stock_quantity < item.quantity:
                    raise ValidationError(f"Not enough stock for {variant.product.name} - {variant.option_combination}")

                # ✅ Create OrderItem
                OrderItem.objects.create(
                    order=order,
                    product_variant=variant,
                    quantity=item.quantity,
                    price=variant.product.price
                )

                # ✅ Update Stock
                if variant.stock_control == "finite":
                    variant.stock_quantity -= item.quantity
                    variant.save()

            # ✅ Calculate Total
            order.calculate_total()
            
            # ✅ Clear Cart
            self.items.all().delete()
            self.status = 'checked_out'
            self.expires_at = timezone.now()
            self.save()

            print(f"🛒 Checkout complete! Order {order.id} has been created.")

        return order

    def cancel_checkout(self):
        """ Restore stock and mark the cart as open """
        if self.status != 'pending_payment':
            raise ValueError("Cart is not pending payment")

        with transaction.atomic():
            for item in self.items.select_related('product_variant'):
                variant = item.product_variant
                if variant.stock_control == "finite":
                    variant.stock_quantity += item.quantity
                    variant.save()
            
            self.status = 'open'
            self.save()
            print(f"🔄 Cart {self.id} checkout canceled. Stock restored.")

    def set_expiration(self, hours=1):
        """ Sets an expiration time for the cart. Default is 1 hour. """
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=hours)
            self.save()

    def is_expired(self):
        """ Checks if the cart is expired. """
        return self.expires_at and timezone.now() >= self.expires_at

    def expire(self):
        """ Marks the cart as expired and restores stock. """
        if not self.is_expired():
            return

        self.status = 'expired'
        for item in self.items.all():
            variant = item.product_variant
            if variant.stock_control == "finite":
                variant.stock_quantity += item.quantity
                variant.save()
                print(f"🔄 Restored stock for {variant}: {variant.stock_quantity} remaining.")
        
        self.save()


class CartItem(models.Model):
    """
    Represents an individual item in the shopping cart.
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    option_values = models.ManyToManyField(ProductOptionValue, blank=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ('cart', 'product_variant')

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} ({self.product_variant.sku})"

    def get_total_price(self):
        """
        Calculate the total price for this cart item.
        """
        return self.product_variant.product.price * self.quantity

    def get_image(self):
        """
        Fetches the primary image of the product variant if it exists.
        """
        primary_image = ProductImage.objects.filter(product=self.product_variant.product, is_primary=True).first()
        if primary_image:
            return primary_image.image.url
        return '/static/images/default-product-image.png'  # Fallback if no image is set

