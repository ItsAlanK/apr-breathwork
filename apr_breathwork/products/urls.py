from django.urls import path
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('account_required', views.product_detail, name='account_required'),
    path('add', views.add_product, name='add_product'),
    path('add/<variant>', views.add_product, name='add_product'),
]
