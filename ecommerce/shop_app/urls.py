
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("store/", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("order-complete/", views.order_complete, name="order_complete"),
    path("place-order/", views.place_order, name="place_order"),
    path("product-detail/", views.product_detail, name="product_detail"),
    path("register/", views.register, name="register"),
    path("search-result/", views.search_result, name="search_result"),
    path("signin/", views.signin, name="signin"),
]