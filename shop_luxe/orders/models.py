from django.db import models
from django.db.models import JSONField
from accounts.models import User
from products.models import ProductVariant

class Order(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('PROCESSING', 'Processing'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')]
    PAYMENT_STATUS_CHOICES = [('PENDING', 'Pending'), ('PAID', 'Paid'), ('FAILED', 'Failed'), ('REFUNDED', 'Refunded')]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    shipping_address = JSONField()
    
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    ordered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username if self.user else 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        if self.variant and self.variant.product:
            return f"{self.quantity} x {self.variant.product.name} in Order {self.order.id}"
        return f"{self.quantity} x [Deleted Product] in Order {self.order.id}"   

    def save(self, *args, **kwargs):
        if self.price is None and self.variant:
            self.price = self.variant.price
        super().save(*args, **kwargs) 
    
    class Meta:
         unique_together = ('order', 'variant') 

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'pending'),
        ('COMPLETED', 'completed'),
        ('FAILED', 'failed'),
        ('REFUNDED', 'refunded'),
    ]

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    gateway = models.CharField(max_length=50) 

    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    gateway_response = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - Status: {self.get_status_display()}"

    class Meta:
        ordering = ('-created_at',)