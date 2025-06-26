# carts/urls.py

from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

urlpatterns = router.urls
