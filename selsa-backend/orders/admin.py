from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Inline admin configuration for OrderItem.
    Allows direct management of OrderItems within the Order admin page.
    """
    model = OrderItem
    #raw_id_fields = ['product_variant']
    readonly_fields = ['price', 'get_total_price']
    extra = 0
    verbose_name = "Order Item"
    verbose_name_plural = "Order Items"

    def get_total_price(self, obj):
        return f"${obj.get_total_price():,.2f}"
    get_total_price.short_description = 'Total Price'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order management.
    """
    list_display = (
        'id', 
        'user', 
        'status', 
        'created_at', 
        'updated_at', 
        'total_amount'
    )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'id', 'status')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]

    fieldsets = (
        ("Order Information", {
            'fields': ('user', 'status', 'total_amount', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        """
        Override save_model to automatically calculate the total.
        """
        super().save_model(request, obj, form, change)
        obj.calculate_total()
