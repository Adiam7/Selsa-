# orders/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Order, OrderItem,Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from rest_framework.decorators import action
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def create_payment_intent(self, request, pk=None):
        """
        Create Stripe PaymentIntent and initiate payment.
        """
        try:
            order = self.get_object()
            if not order.total_amount:
                return Response({"error": "Order has no total amount."}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Create Stripe PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(order.total_amount * 100),  # Stripe expects cents
                currency='usd',
                payment_method_types=['card']
            )

            # ✅ Create Payment Object
            payment = Payment.objects.create(
                order=order,
                stripe_payment_intent=payment_intent['id'],
                amount=order.total_amount,
                status='pending'
            )

            serializer = PaymentSerializer(payment)
            return Response({
                'client_secret': payment_intent['client_secret'],
                'payment': serializer.data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
