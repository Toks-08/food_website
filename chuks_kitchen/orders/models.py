from django.db import models
from accounts.models import CustomUser
from menu.models import MenuItem
from django.utils import timezone

# Create your models here.
class Order (models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentStatus(models.TextChoices):
        UNPAID = "UNPAID", "Unpaid"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=Status.choices,
     default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices,
     default='UNPAID')
    cancelled_by = models.ForeignKey(
    CustomUser,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="cancelled_orders"
)

    cancel_reason = models.TextField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

 
    def __str__(self):
        return f"Order {self.order_number}"
    

    def cancel(self, user, reason=None):
        if self.user != user:
            raise ValueError("You cannot cancel someone's order")

        if self.status == self.Status.CANCELLED:
            raise ValueError("Order already cancelled.")

        if self.status != self.Status.PENDING:
            raise ValueError("Order cannot be cancelled at this stage.")

        self.status = self.Status.CANCELLED
        self.cancelled_by = user
        self.cancel_reason = reason
        self.cancelled_at = timezone.now()

        # Restore stock
        for item in self.order_items.all():
            item.menu_item.stock += item.quantity
            item.menu_item.save()

        # Handle refund
        if self.payment_status == self.PaymentStatus.PAID:
            self.payment_status = self.PaymentStatus.REFUNDED

        self.save()


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