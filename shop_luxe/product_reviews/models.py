from django.db import models
from accounts.models import User

class Review(models.Model):
    product_id = models.CharField(max_length=24)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product_id', 'user')

    def __str__(self):
        return f"Review for Product {self.product_id} by {self.user.username}"
