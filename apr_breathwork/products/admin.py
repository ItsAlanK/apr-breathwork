from django.contrib import admin
from .models import Category, Product, ProductVariant


class CategoryAdmin(admin.ModelAdmin):
    """ Set list display items for categories in admin """
    list_display = (
        'friendly_name',
        'name',
    )


class ProductAdmin(admin.ModelAdmin):
    """ Set list display items for products in admin """
    list_display = (
        'name',
        'category',
        'price',
        'duration',
        'image',
    )

    ordering = ('name',)


class ProductVariantAdmin(admin.ModelAdmin):
    """ Set list display items for product variants in admin """
    list_display = (
        'product',
        'date',
        'time',
        'attendance_limit',
        'places_sold'
    )

    readonly_fields=('places_sold',)
    ordering = ('date', 'time')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
