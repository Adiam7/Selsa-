from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductOptionTypeViewSet, ProductVariantViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')
router.register(r'option-types', ProductOptionTypeViewSet)
router.register(r'variants', ProductVariantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
