from django.db import models
from accounts.models import CustomUser
from menu.models import MenuItem

# Create your models here.
class Order (models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('SHIPPED','Shipped'),
        ('DELIVERED','Delivered'),
        ('CANCELLED','Cancelled')
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('UNPAID', 'Unpaid'),
        ('PAID','Paid'),
        ('FAILED','Failed'),
        ('REFUNDED','Refunded'),
    ], default='UNPAID')

    def __str__(self):
        return f"Order {self.order_number}"
    def update_total(self):
        total = sum(
        item.get_subtotal() for item in self.order_items.all()
    )
        self.total_amount = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name= 'order_items')
    price_at_purchase=models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        return self.price_at_purchase * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"