from rest_framework import serializers
from .models import Payment
from django.utils import timezone
import uuid

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id','order','payment_method','transaction_id','amount','status','paid_at','created_at']
        read_only_fields = ['status', 'transaction_id', 'paid_at', 'created_at']

    def validate(self, data):
        order = data['order']

        # Ensure user owns the order
        if order.user != self.context['request'].user:
            raise serializers.ValidationError("You can only pay for your own orders.")
        
        # Check if the payment amount matches the order total
        if data['amount'] != order.total_amount:
            raise serializers.ValidationError(
                f"Incorrect amount. Order total is {order.total_amount}."
            )

        # Ensure order is unpaid
        if hasattr(order, 'payment'):
            raise serializers.ValidationError("This order already has a payment.")

        return data
    
    def create(self, validated_data):
        # Generate a unique transaction ID automatically
        validated_data['transaction_id'] = f"CHKS-{uuid.uuid4().hex[:10].upper()}"
        validated_data['status'] = 'COMPLETED'
        validated_data['paid_at'] = timezone.now()
        
        payment = super().create(validated_data)
        
        # Logic Tip: Automatically update the Order status to 'PAID'
        order = payment.order
        order.payment_status = 'PAID' # Or however you named the field in Order model
        order.save()
        
        return payment