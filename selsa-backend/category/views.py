from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from category.models import Category
from .serializers import CategorySerializer
from products.serializers import ProductSerializer  # Adjust import as needed

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing categories.
    """
    queryset = Category.objects.prefetch_related('children', 'products').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'slug']

    @action(detail=False, url_path='slug/(?P<slug>[^/.]+)', methods=['get'])
    def retrieve_by_slug(self, request, slug=None):
        """
        Custom action to retrieve a category by its slug.
        """
        try:
            category = Category.objects.prefetch_related('children', 'products').get(slug=slug)
            serializer = self.get_serializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = category.products.all()  # or a queryset if you use related_name
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='(?P<slug>[^/.]+)/products', methods=['get'])
    def products_by_slug(self, request, slug=None):
        try:
            category = Category.objects.get(slug=slug)
            products = category.products.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=404)
