from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id','menu_item','price_at_purchase','quantity']
        read_only_fields = ['id', 'price_at_purchase', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order_items', many=True)
    class Meta:
        model = Order
        fields = ['id','total_amount','status','order_number','user','payment_status','created_at','updated_at','items']
        read_only_fields = ['id','total_amount','status','order_number','payment_status','created_at','updated_at']



        
def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        # 1. Create the parent Order
        order = Order.objects.create(**validated_data)

        # 2. Loop through items and "Freeze" the price
        for item_data in items_data:
            menu_item = item_data['menu_item']
            OrderItem.objects.create(
                order=order, 
                menu_item=menu_item,
                price_at_purchase=menu_item.price, # Set the price from the MenuItem model
                quantity=item_data['quantity']
            )

        # 3. Recalculate the grand total
        order.update_total()
        return order