from django.contrib.sessions.models import Session
from .models import Product, ProductOptionType, ProductOptionValue
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class CartService:
    def __init__(self, request):
        """
        Initialize the cart service. Either use the session data or create a new cart.
        """
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add_item(self, product_slug, option_values, quantity):
        """
        Add an item to the cart, using ProductOptionValue to define selected options.
        """
        product = Product.objects.get(slug=product_slug)
        option_key = self._generate_option_key(option_values)

        if option_key in self.cart:
            # If product with specific options already exists, just update the quantity
            self.cart[option_key]['quantity'] += quantity
        else:
            # If product with these options doesn't exist in cart, add it
            self.cart[option_key] = {
                'product_slug': product_slug,
                'quantity': quantity,
                'option_values': option_values,
                'price': float(product.price),
                'name': product.name,
                'image': self._get_product_image(product, option_values)
            }

        self._save_cart()

    def remove_item(self, product_slug, option_values):
        """
        Remove an item from the cart based on the product and option values.
        """
        option_key = self._generate_option_key(option_values)
        if option_key in self.cart:
            del self.cart[option_key]
            self._save_cart()

    def update_item_quantity(self, product_slug, option_values, quantity):
        """
        Update the quantity of an item in the cart.
        """
        option_key = self._generate_option_key(option_values)
        if option_key in self.cart:
            self.cart[option_key]['quantity'] = quantity
            self._save_cart()

    def get_cart_items(self):
        """
        Retrieve all items in the cart, with details for each product and its options.
        """
        items = []
        for key, value in self.cart.items():
            product = Product.objects.get(slug=value['product_slug'])
            items.append({
                'product': product.name,
                'quantity': value['quantity'],
                'price': value['price'],
                'option_values': value['option_values'],
                'image': value['image']
            })
        return items

    def get_cart_totals(self):
        """
        Calculate the total price of the cart, including taxes, shipping, etc.
        """
        subtotal = sum(item['price'] * item['quantity'] for item in self.cart.values())
        tax = subtotal * Decimal(0.1)  # Example: 10% tax rate
        shipping = Decimal(5.00)  # Flat shipping fee
        total = subtotal + tax + shipping
        return subtotal, tax, shipping, total

    def _generate_option_key(self, option_values):
        """
        Generate a unique key for each product based on the selected options.
        """
        option_str = "_".join([f"{opt}={val}" for opt, val in option_values.items()])
        return option_str

    def _get_product_image(self, product, option_values):
        """
        Get the correct image for the product based on the selected option values.
        """
        option_types = ProductOptionType.objects.all()
        # You can refine this logic to pick an image that matches the option values
        return "/static/images/default-image.png"  # Replace with actual image logic

    def _save_cart(self):
        """
        Save the cart back to the session.
        """
        self.session['cart'] = self.cart
        self.session.modified = True
