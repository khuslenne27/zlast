from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'category_name',
        'slug',
        'description',
    )

    prepopulated_fields = {
        'slug': ('category_name',)
    }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'product_name',
        'price',
        'stock',
        'category',
        'is_available',
        'created_date',
        'modified_date',
    )

    prepopulated_fields = {
        'slug': ('product_name',)
    }

    list_filter = (
        'category',
        'is_available',
    )

    search_fields = (
        'product_name',
        'description',
    )