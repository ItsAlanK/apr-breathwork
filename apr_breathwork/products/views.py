from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, ProductVariant
from .forms import ProductForm, ProductVariantForm


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


def add_product(request, variant=None):
    """ Add a product or variant to the store """

    if variant:
        if request.method == 'POST':
            form = ProductVariantForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully added Product Variant!')
                return redirect(reverse('add_product'))
            else:
                messages.error(request,
                    'Failed to add product variant. Please check form details.'
                )
                print('hello')
        else:
            variant_form = ProductVariantForm()

        template = 'products/add-product.html'
        context = {
            'form': variant_form,
        }

        return render(request, template, context)
    else:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully added Product!')
                return redirect(reverse('add_product'))
            else:
                messages.error(request, 'Failed to add product. Please check form details.')
        else:
            form = ProductForm()

    template = 'products/add-product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product """

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please check form details.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit-product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

def edit_product_variant(request, product_id, variant_id=None):
    """ Edit a variant """

    if variant_id:
        product = get_object_or_404(Product, pk=product_id)
        variant = get_object_or_404(ProductVariant, pk=variant_id)

        if request.method == 'POST':
            form = ProductVariantForm(request.POST, instance=variant)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated product variant.')
                return redirect(reverse('product_detail', args=[product.id]))
            else:
                messages.error(request, 'Failed to update product. Please check form details.')
        else:
            form = ProductVariantForm(instance=variant)
            messages.info(request, f'You are editing {variant}')

        template = 'products/edit-product-variant.html'
        context = {
            'product': product,
            'variant': variant,
            'form': form,
        }

        return render(request, template, context)
    else:
        product = get_object_or_404(Product, pk=product_id)
        variants = ProductVariant.objects.filter(product=product)
        base_url = f'/products/edit/variant/{product_id}'

        if request.method == 'POST':
            selected_variant = request.POST.get('variant')
            return redirect('edit_product_variant', product_id, selected_variant)

        template = 'products/edit-product-variant.html'
        context = {
            'product': product,
            'variants': variants,
            'base_url': base_url,
        }

        return render(request, template, context)
