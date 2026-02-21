from rest_framework import viewsets, permissions
from django.utils import timezone
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # User only sees their own payments
        return Payment.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        payment = serializer.save()

        # Simulate successful payment
        payment.status = 'SUCCESS'
        payment.transaction_id = f"TXN-{payment.id}"
        payment.paid_at = timezone.now()
        payment.save()

        # Update order payment status
        payment.order.payment_status = 'PAID'
        payment.order.save()