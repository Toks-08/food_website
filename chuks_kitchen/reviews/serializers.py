from rest_framework import serializers
from .models import Review
from orders.models import OrderItem


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Review
        fields = ['id','user','menu_item','order','rating','comment','created_at','updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        menu_item = data['menu_item']
        order = data['order']

        # Ensure order belongs to user
        if order.user != user:
            raise serializers.ValidationError(
                "You can only review your own orders."
            )

        # Ensure menuitem exists in that order
        if not OrderItem.objects.filter(order=order, menuitem=menu_item).exists():
            raise serializers.ValidationError(
                "This product was not purchased in this order."
            )

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)