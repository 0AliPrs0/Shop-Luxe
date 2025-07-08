from django.contrib import admin
from .models import Order, OrderItem

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

