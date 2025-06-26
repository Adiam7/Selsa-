# carts/utils.py
from .models import Cart

def process_payment(cart_id):
    """
    Mock payment process.
    In real-world scenarios, integrate this with Stripe, PayPal, etc.
    """
    try:
        cart = Cart.objects.get(id=cart_id)

        # Mocking payment success (replace with real payment logic)
        payment_success = True  

        if payment_success:
            cart.status = 'checked_out'
            cart.save()
            print(f"✅ Payment succeeded for Cart {cart_id}")
        else:
            cart.status = 'payment_failed'
            cart.save()
            print(f"❌ Payment failed for Cart {cart_id}")

    except Cart.DoesNotExist:
        print("⚠️ Cart not found for payment processing.")
