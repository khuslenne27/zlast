
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import Cart, CartItem
from store.models import Product


def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        request.session.create()
        cart = request.session.session_key

    return cart


@require_POST
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not product.is_available or product.stock <= 0:
        messages.error(request, "Энэ бараа дууссан байна.")
        return redirect('cart')

    with transaction.atomic():
        cart, created = Cart.objects.get_or_create(
            cart_id=_cart_id(request)
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': 0,
                'is_active': True
            }
        )

        # Product Detail-ээс нэмэх үед давхардуулахгүй
        if request.POST.get('source') == 'product_detail':
            if cart_item.quantity > 0:
                messages.warning(
                    request,
                    "Энэ бараа аль хэдийн сагсанд байна."
                )
                return redirect(
                    'product_detail',
                    category_slug=product.category.slug,
                    product_slug=product.slug
                )

        if cart_item.quantity >= product.stock:
            messages.warning(
                request,
                "Барааны үлдэгдлээс илүү нэмэх боломжгүй."
            )
            return redirect('cart')

        cart_item.quantity += 1
        cart_item.is_active = True
        cart_item.save()

    return redirect('cart')


@require_POST
def remove_cart(request, product_id):
    with transaction.atomic():
        cart = Cart.objects.filter(
            cart_id=_cart_id(request)
        ).first()

        if cart:
            cart_item = CartItem.objects.filter(
                cart=cart,
                product_id=product_id
            ).first()

            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()

    return redirect('cart')


@require_POST
def remove_cart_item(request, product_id):
    cart = Cart.objects.filter(
        cart_id=_cart_id(request)
    ).first()

    if cart:
        CartItem.objects.filter(
            cart=cart,
            product_id=product_id
        ).delete()

    return redirect('cart')


def cart(request):
    total = 0
    quantity = 0
    cart_items = []

    current_cart = Cart.objects.filter(
        cart_id=_cart_id(request)
    ).first()

    if current_cart:
        cart_items = CartItem.objects.filter(
            cart=current_cart,
            is_active=True
        ).select_related('product')

        for cart_item in cart_items:
            total += cart_item.sub_total()
            quantity += cart_item.quantity

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }

    return render(request, 'carts/cart.html', context)
