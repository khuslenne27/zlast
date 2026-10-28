
from .models import Cart, CartItem


def cart_counter(request):
    cart_count = 0

    session_key = request.session.session_key

    if session_key:
        cart = Cart.objects.filter(
            cart_id=session_key
        ).first()

        if cart:
            cart_items = CartItem.objects.filter(
                cart=cart,
                is_active=True
            )

            cart_count = sum(
                item.quantity for item in cart_items
            )

    return {
        'cart_count': cart_count
    }
