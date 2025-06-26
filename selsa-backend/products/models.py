from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.timezone import now
import uuid # For UUID generation
from category.models import Category  # Import the Category model
from django.contrib.postgres.fields import JSONField  # or just models.JSONField in Django 3.1+
from django.utils.crypto import get_random_string

# Product Model
class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name="products")
    availability = models.BooleanField(default=True, help_text="Is the product available for sale?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def sync_availability(self):
        """
        Syncs the product availability based on its variants.
        If any variant is available, the product is available.
        """
        if self.variants.filter(is_out_of_stock=False).exists():
            self.availability = True
        else:
            self.availability = False
        self.save(update_fields=['availability'])
        
# Product Image Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", db_index=True)
    image = models.ImageField(upload_to="product_images/")
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, blank=True, null=True)  # Optional alt text for SEO
    option_type = models.ForeignKey('ProductOptionType', on_delete=models.CASCADE, null=True, blank=True)
    option_value = models.ForeignKey('ProductOptionValue', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # if self.option_type and self.option_value:
        #     return f"{self.product.name} - {self.option_type.name}: {self.option_value.value} Image"
        # return f"{self.product.name} Image"
        return f"Image for {self.product.name} ({'Main' if self.is_primary else 'Gallery'})"

# Product FieldType Model
class FieldType(models.Model):
    """Defines how options are displayed (Dropdown, Radio, Checkbox, Size)."""
    # This is a placeholder for the field type. You can define your own field types.
    # For example: Dropdown, Radio, Checkbox, Size, etc.
    field_type = models.CharField(max_length=100, unique=True)      
    django_widget = models.CharField(max_length=255)  # e.g., "django.forms.widgets.Select"

    def __str__(self):
        return self.field_type


# Product Option Types and Values
class ProductOptionType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., 'Color', 'Size'
    field_type = models.CharField(max_length=100)  # Removed ForeignKey to FieldType for simplification

    def __str__(self):
        return self.name


class ProductOptionValue(models.Model):
    option_type = models.ForeignKey(ProductOptionType, on_delete=models.CASCADE, related_name='values')
    #🔹 Replace "Default Value" with something more meaningful if you have a logical default, like "Not Specified" or "Unknown".
    value = models.CharField(max_length=100, default='Unknown')

    class Meta:
        unique_together = ('option_type', 'value')  # Prevent duplicate values
    def __str__(self):
        return f"{self.option_type.name} - {self.value}"


# Stock Control Options
class StockControl(models.TextChoices):
    INFINITE = "infinite", "Unlimited Stock"
    FINITE = "finite", "Limited Stock"
    PREORDER = "preorder", "Preorder Available"

# Product Variant Model
# products/models.py

class ProductVariant(models.Model):
    """Represents a specific variant of a product based on its options."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", db_index=True)
    option_values = models.ManyToManyField(ProductOptionValue)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_control = models.CharField(max_length=20, choices=StockControl.choices, default=StockControl.FINITE)
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    option_combination = models.CharField(max_length=255, blank=True, null=True)

    
    # New fields 🚀
    low_stock_threshold = models.PositiveIntegerField(default=5)
    is_low_stock = models.BooleanField(default=False)
    is_out_of_stock = models.BooleanField(default=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'option_combination'], name='unique_product_variant_combination')
        ]
        ordering = ['product', 'option_combination']

    def is_available(self):
        """Determine if the variant is available for purchase."""
        return (
            self.stock_control == StockControl.INFINITE or
            (self.stock_control == StockControl.FINITE and self.stock_quantity > 0) or
            self.stock_control == StockControl.PREORDER
        )

    def __str__(self):
        if not self.pk:
            return "Unsaved ProductVariant"
        values = ", ".join([f"{v.option_type.name}: {v.value}" for v in self.option_values.all()])
        status = "Available" if self.is_available() else "Out of Stock"
        return f"{self.product.name} - {values} [{status}]"
    
    def update_stock_status(self):
        """
        Updates the low stock and out of stock statuses.
        """
        if self.stock_control == "finite":
            self.is_low_stock = self.stock_quantity <= self.low_stock_threshold and self.stock_quantity > 0
            self.is_out_of_stock = self.stock_quantity == 0
            self.save(update_fields=['is_low_stock', 'is_out_of_stock'])




