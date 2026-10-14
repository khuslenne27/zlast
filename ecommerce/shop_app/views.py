from django.shortcuts import render
from .models import Category, Product


def index(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    product_count = products.count()

    context = {
        "products": products,
        "categories": categories,
        "product_count": product_count,
    }

    return render(request, "index.html", context)


def store(request):
    products = list(Product.objects.raw(
        "SELECT * FROM store_product WHERE is_available = %s",
        [True]
    ))

    categories = Category.objects.all()
    product_count = len(products)

    context = {
        "products": products,
        "categories": categories,
        "product_count": product_count,
    }

    return render(request, "store.html", context)


def cart(request):
    return render(request, "cart.html")


def dashboard(request):
    return render(request, "dashboard.html")


def order_complete(request):
    return render(request, "order_complete.html")


def place_order(request):
    return render(request, "place-order.html")


def product_detail(request):
    products = Product.objects.all()
    return render(request, "product-detail.html", {
        "products": products
    })


def register(request):
    return render(request, "register.html")


def search_result(request):
    keyword = request.GET.get("keyword", "").strip()

    if keyword:
        products = Product.objects.filter(
            product_name__icontains=keyword,
            is_available=True
        )
    else:
        products = Product.objects.none()

    context = {
        "products": products,
        "product_count": products.count(),
        "keyword": keyword,
    }

    return render(request, "search-result.html", context)


def signin(request):
    return render(request, "signin.html")