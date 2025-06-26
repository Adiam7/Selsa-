from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductImage,
    ProductOptionType,
    ProductOptionValue,
    ProductVariant,
    FieldType
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "availability", "created_at")
    search_fields = ("name", "sku")
    list_filter = ("availability", "categories")
    inlines = [ProductImageInline, ProductVariantInline]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(ProductOptionType)
class ProductOptionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "field_type")

@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):
    list_display = ("option_type", "value")

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "option_combination", "stock_quantity", "stock_control", 'is_available')
    list_filter = ("stock_control",)
    search_fields = ("product__name", 'option_combination', 'sku')
    readonly_fields = ('option_combination', 'sku')  # Prevent editing directly

    def is_available(self, obj):
        """Display availability status in the admin list view."""
        return obj.is_available()
    is_available.boolean = True  # Shows a green check or red cross in the admin
    
@admin.register(FieldType)
class FieldTypeAdmin(admin.ModelAdmin):
    list_display = ("field_type", "django_widget")
    search_fields = ("field_type",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
