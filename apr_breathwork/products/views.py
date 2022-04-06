from django.shortcuts import render
from .models import Product


def products(request):
    """ View which returns products list """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
