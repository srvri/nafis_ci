#apis/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,  SizeViewSet,
    MaterialViewSet, ApparelViewSet, ApparelImageViewSet,
    SlideShowViewSet, ContactViewSet, CartItemViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('sizes', SizeViewSet)
router.register('materials', MaterialViewSet)
router.register('apparels', ApparelViewSet)
router.register('apparel-images', ApparelImageViewSet)
router.register('slideshows', SlideShowViewSet)
router.register('contacts', ContactViewSet)
router.register('cart-items', CartItemViewSet)

urlpatterns = router.urls
