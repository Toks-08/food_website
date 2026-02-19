from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, MenuItemView, MenuItemVariationView

router = DefaultRouter()
router.register(r'categories', CategoryView)
router.register(r'menu', MenuItemView)
router.register(r'menu-variations', MenuItemVariationView)

urlpatterns = [
    path('', include(router.urls)),
]