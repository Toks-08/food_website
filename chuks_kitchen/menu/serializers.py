from .models import Category,MenuItem,MenuItemVariation
from rest_framework import serializers


class MenuItemVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model =  MenuItemVariation
        fields = ['menu_item', 'name', 'price', 'is_available']


class MenuItemSerializer(serializers.ModelSerializer):
    variations = MenuItemVariationSerializer(many=True, read_only=True)
    class Meta:
        model = MenuItem
        fields = ['name', 'category', 'description', 'price','image','variations', 'is_available', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'image','items','slug']

