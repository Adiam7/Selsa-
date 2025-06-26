# services/product_service.py

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from products.models import Product, ProductImage, ProductVariant, ProductOptionValue
from typing import List, Dict, Optional


class ProductService:
    """
    Service Layer for Product Operations.
    This handles business logic, validation, and database operations 
    related to Product creation, updates, retrieval, and deletion.
    """

    @staticmethod
    @transaction.atomic
    def create_product(data: Dict, images: Optional[List[Dict]] = None, variants: Optional[List[Dict]] = None) -> Product:
        """
        Create a new Product with optional images and variants.

        Args:
            data (Dict): Product details.
            images (List[Dict], optional): List of image data dictionaries.
            variants (List[Dict], optional): List of variant data dictionaries.

        Returns:
            Product: The created product instance.
        """
        product = Product.objects.create(**data)

        if images:
            ProductImage.objects.bulk_create([
                ProductImage(product=product, **image_data) for image_data in images
            ])

        if variants:
            ProductVariant.objects.bulk_create([
                ProductVariant(product=product, **variant_data) for variant_data in variants
            ])

        return product

    @staticmethod
    @transaction.atomic
    def update_product(product_id: str, data: Dict) -> Optional[Product]:
        """
        Update an existing Product.
        
        Args:
            product_id (str): The UUID of the product to update.
            data (Dict): Updated product details.

        Returns:
            Optional[Product]: The updated product instance or None if not found.
        """
        try:
            product = Product.objects.get(id=product_id)
            for key, value in data.items():
                setattr(product, key, value)
            product.save()
            return product
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_product_details(product_id: str) -> Optional[Product]:
        """
        Retrieve product details, including images and variants.

        Args:
            product_id (str): The UUID of the product.

        Returns:
            Optional[Product]: The product instance if found, else None.
        """
        try:
            return Product.objects.prefetch_related('images', 'variants').get(id=product_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_products(filters: Optional[Dict] = None) -> List[Product]:
        """
        Retrieve all products, optionally filtered.

        Args:
            filters (Dict, optional): Filtering options.

        Returns:
            List[Product]: List of filtered products.
        """
        queryset = Product.objects.prefetch_related('images', 'variants')
        if filters:
            queryset = queryset.filter(**filters)
        return list(queryset)

    @staticmethod
    @transaction.atomic
    def update_stock(product_id: str, quantity: int) -> Optional[int]:
        """
        Update the stock quantity of a product.

        Args:
            product_id (str): The UUID of the product.
            quantity (int): Quantity to add or subtract.

        Returns:
            Optional[int]: The new stock quantity if successful, else None.
        """
        try:
            product = Product.objects.select_for_update().get(id=product_id)
            product.stock_quantity = max(0, product.stock_quantity + quantity)
            product.save()
            return product.stock_quantity
        except ObjectDoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def delete_product(product_id: str) -> bool:
        """
        Delete a product and its associated images and variants.

        Args:
            product_id (str): The UUID of the product.

        Returns:
            bool: True if successful, False if not found.
        """
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return True
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def attach_images(product: Product, images: List[Dict]) -> None:
        """
        Attach images to a product.

        Args:
            product (Product): Product instance.
            images (List[Dict]): List of image data dictionaries.
        """
        ProductImage.objects.bulk_create([
            ProductImage(product=product, **image_data) for image_data in images
        ])

    @staticmethod
    def attach_variants(product: Product, variants: List[Dict]) -> None:
        """
        Attach variants to a product.

        Args:
            product (Product): Product instance.
            variants (List[Dict]): List of variant data dictionaries.
        """
        ProductVariant.objects.bulk_create([
            ProductVariant(product=product, **variant_data) for variant_data in variants
        ])
