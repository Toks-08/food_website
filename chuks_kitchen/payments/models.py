from django.db import models
from orders.models import Order
import uuid


class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('CARD', 'Card'),
        ('TRANSFER', 'Bank Transfer'),
        ('CASH', 'Cash'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField( Order,on_delete=models.CASCADE,related_name='payment')
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100,blank=True,null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='PENDING')
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.order_number}"