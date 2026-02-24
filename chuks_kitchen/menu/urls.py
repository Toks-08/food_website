from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, MenuItemView, MenuItemVariationView

router = DefaultRouter()
router.register(r'categories', CategoryView)
router.register(r'foods', MenuItemView)
router.register(r'foods-variations', MenuItemVariationView)

urlpatterns = [
    path('', include(router.urls)),
]