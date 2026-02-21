from django.db import models
from django.conf import settings
from menu.models import MenuItem
from orders.models import Order


class Review(models.Model):

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews')
    menu_item = models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name='reviews')
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'menu_item', 'order')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.product.name} ({self.rating})"