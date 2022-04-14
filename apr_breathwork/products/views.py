from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, ProductVariant


def products(request):

    """ View which returns products list """

    products = Product.objects.all()
    query = None
    category = None

    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(category__name=category)
            category = Category.objects.filter(name=category)
            if not products:
                messages.error(request, "No products in this Category.")

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "No search query entered.")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_category': category,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):

    """ View which returns detailed view of the requested product """

    product = get_object_or_404(Product, pk=product_id)
    variants = ProductVariant.objects.filter(product=product)

    context = {
            'product': product,
            'variants': variants,
        }

    if product.account_required:
        if request.user.is_authenticated:
            return render(request, 'products/product-detail.html', context)
        else:
            return render(request, 'products/account-required.html', context)
    else:
        return render(request, 'products/product-detail.html', context)
