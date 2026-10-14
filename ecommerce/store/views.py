from django.shortcuts import render
from .models import Product, Category


def home(request):
    store_products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'store_products': store_products,
        'categories': categories,
    }

    return render(
        request,
        'home.html',
        context
    )


def store(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    # Search
    keyword = request.GET.get('keyword', '')

    if keyword:
        products = products.filter(
            product_name__icontains=keyword
        )

    product_count = products.count()

    context = {
        'store_products': products,
        'categories': categories,
        'product_count': product_count,
        'keyword': keyword,
    }

    return render(
        request,
        'store/store.html',
        context
    )