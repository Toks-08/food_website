from django.shortcuts import render
from .serializers import CategorySerializer,MenuItemSerializer,MenuItemVariationSerializer
from .models import Category,MenuItem,MenuItemVariation
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly

# Create your views here.
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('items__variations').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class MenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrReadOnly]

class MenuItemVariationView(viewsets.ModelViewSet):
    queryset = MenuItemVariation.objects.all()
    serializer_class = MenuItemVariationSerializer
    permission_classes = [IsAdminOrReadOnly]
