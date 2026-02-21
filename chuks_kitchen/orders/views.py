from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderSerializer
from menu.models import MenuItem


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own orders
        return Order.objects.filter(user=self.request.user)

#transaction.atomic ensures everything either fails or saves completely, no partial data
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        items = request.data.get("items", [])

        if not items:
            return Response(
                {"error": "Order must contain at least one item."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create empty order first
        order = Order.objects.create(
            user=request.user,
            order_number=f"ORD-{Order.objects.count() + 1}"
        )

        # Create order items
        for item in items:
            try:
                menu_item = MenuItem.objects.get(id=item["menu_item"])
            except MenuItem.DoesNotExist:
                return Response(
                    {"error": "Menu item not found."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item["quantity"],
                price_at_purchase=menu_item.price  # copy price safely from database
            )

        # Update total
        order.update_total()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)