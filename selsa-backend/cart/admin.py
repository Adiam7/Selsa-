from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Number of empty forms to show in the inline formset
    fields = ['product_variant', 'quantity', 'option_values', 'get_image']
    
    readonly_fields = ['get_image']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at', 'status']
    inlines = [CartItemInline]
    search_fields = ['user__username']
    list_filter = ['status']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
