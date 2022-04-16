from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('account_required', views.product_detail, name='account_required'),
    path('add', views.add_product, name='add_product'),
    path('add/<variant>', views.add_product, name='add_product'),
    path('edit/<int:product_id>', views.edit_product, name='edit_product'),
    path('edit/variant/<int:product_id>', views.edit_product_variant, name='edit_product_variant'),
    path('edit/variant/<int:product_id>/<int:variant_id>',
        views.edit_product_variant,
        name='edit_product_variant'
        ),
    path('delete/<int:product_id>', views.delete_product, name='delete_product'),
    path('delete/variant/<int:variant_id>', views.delete_variant, name='delete_variant'),
]
