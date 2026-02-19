from django.contrib import admin
from .models import Category, MenuItem, MenuItemVariation

admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(MenuItemVariation)