
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Product, Category
from carts.models import CartItem


def home(request):
    store_products = Product.objects.all().order_by('-id')[:8]
    categories = Category.objects.all()

    context = {
        'store_products': store_products,
        'categories': categories,
    }

    return render(request, 'home.html', context)


def store(request, category_slug=None):
    products = Product.objects.all()
    categories = Category.objects.all()

    selected_category = None

    if category_slug:
        selected_category = get_object_or_404(
            Category,
            slug=category_slug
        )
        products = products.filter(
            category=selected_category
        )

    keyword = request.GET.get('keyword', '').strip()

    if keyword:
        products = products.filter(
            product_name__icontains=keyword
        )

    products = products.order_by('-id')
    product_count = products.count()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    context = {
        'products': paged_products,
        'store_products': paged_products,
        'categories': categories,
        'product_count': product_count,
        'selected_category': selected_category,
        'keyword': keyword,
    }

    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug
    )

    categories = Category.objects.all()

    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    in_cart = CartItem.objects.filter(
        cart__cart_id=session_key,
        product_id=product.id,
        quantity__gt=0
    ).exists()

    context = {
        'product': product,
        'categories': categories,
        'in_cart': in_cart,
    }

    return render(
        request,
        'store/product_detail.html',
        context
    )
