# apps/order/admin.py

# from django.contrib import admin
# from .models import Order, OrderItem

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'total_price', 'status', 'is_paid', 'created_at')
#     list_filter = ('status', 'is_paid')
#     search_fields = ('user__username', 'id')


# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product_variant', 'quantity', 'price')
#     search_fields = ('order__id', 'product_variant__product__name')
