# selsa-backend/products/views.py

from rest_framework import viewsets
from .models import Product, ProductOptionType, ProductVariant
from .serializers import ProductSerializer, ProductOptionTypeSerializer, ProductVariantSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'categories': ['exact'],
        'categories__slug': ['exact'],  # Use your actual related name
    }
    lookup_field = 'slug'

class ProductOptionTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductOptionType.objects.all()
    serializer_class = ProductOptionTypeSerializer

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer


