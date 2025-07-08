from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product_id', 'product_name', 'quantity', 'price', 'variant') 
    readonly_fields = ('product_id', 'product_name', 'quantity', 'price', 'variant')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'payment_status', 'total_amount', 'ordered_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        return False 

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_link', 'amount', 'gateway', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'gateway', 'created_at')
    search_fields = ('transaction_id', 'order__id', 'order__user__username')
    readonly_fields = ('order', 'amount', 'gateway', 'transaction_id', 'gateway_response', 'created_at', 'updated_at')

    def order_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        link = reverse("admin:orders_order_change", args=[obj.order.id])
        return format_html('<a href="{}">Order {}</a>', link, obj.order.id)
    
    order_link.short_description = 'Order'

    def has_add_permission(self, request):
        return False
