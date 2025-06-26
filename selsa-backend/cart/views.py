# carts/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import ProductVariant, ProductOptionValue
from rest_framework.decorators import action
from django.utils import timezone
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from .models import Cart
from .serializers import CartSerializer
from .utils import process_payment

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        """
        Custom action to handle checkout.
        - Moves items from Cart to Order
        - Checks stock availability
        - Deducts stock quantity
        - Clears the cart after checkout
        """
        cart = self.get_object()

        if cart.items.count() == 0:
            return Response({"error": "Cart is empty!"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Validate stock before checkout
        insufficient_stock = []
        for item in cart.items.all():
            if item.product_variant.stock_control == "finite" and item.product_variant.stock_quantity < item.quantity:
                insufficient_stock.append({
                    'product': item.product_variant.product.name,
                    'requested': item.quantity,
                    'available': item.product_variant.stock_quantity
                })
        
        if insufficient_stock:
            return Response({
                "error": "Insufficient stock for some items.",
                "details": insufficient_stock
            }, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Create Order
        order = Order.objects.create(
            user=cart.user,
            status='pending',
            total_amount=cart.get_total()
        )

        # ✅ Transfer items to OrderItem
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_variant=item.product_variant,
                quantity=item.quantity,
                price=item.product_variant.price
            )

            # ✅ Deduct Stock
            if item.product_variant.stock_control == "finite":
                item.product_variant.stock_quantity -= item.quantity
                item.product_variant.save()

        # ✅ Start the payment process        
        try:
            cart.checkout()
            process_payment(cart.id)  # 🔄 Start the payment process
            return Response({"message": "Checkout successful. Payment processing initiated."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # ✅ Clear the cart
        cart.items.all().delete()
        cart.status = 'checked_out'
        cart.expires_at = timezone.now()
        cart.save()

        # ✅ Return the created order
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        """
        Adds an item to the cart, updating quantity if the product already exists.
        """
        cart_id = request.data.get('cart')
        variant_id = request.data.get('product_variant')
        quantity = int(request.data.get('quantity', 1))
        option_values = request.data.get('option_values', [])

        # Get or create the cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart_id=cart_id,
            product_variant_id=variant_id
        )
        
        # Update quantity if exists
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.option_values.set(ProductOptionValue.objects.filter(id__in=option_values))

        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
