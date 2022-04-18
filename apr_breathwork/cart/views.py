from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import ProductVariant, Product


def view_cart(request):
    """ View which returns cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, item_id):
    """ Add selected product to the cart """

    product = get_object_or_404(Product, pk=item_id)
    date = request.POST.get('date')
    time = request.POST.get('time')
    variant = date + "/" + time
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    # Checks if product is in cart already
    # then checks if same variant is in cart
    # if not adds new variant/product to cart
    if item_id in list(cart.keys()):
        if variant in cart[item_id]:
            messages.warning(
                request,
                f"{product.name} for {date} at {time} is already your cart!"
                )
        else:
            cart[item_id] += [variant]
            messages.success(
                request,
                f"{product.name} for {date} at {time} "
                "has been added to your cart!"
                )
    else:
        cart[item_id] = [variant]
        messages.success(
            request,
            f"{product.name} for {date} at {time} has been added to your cart!"
            )

    request.session['cart'] = cart
    return redirect(redirect_url)


def remove_from_cart(request, var_id):
    """ Remove chosen item & variant from cart """

    cart = request.session.get('cart', {})
    variant = get_object_or_404(ProductVariant, pk=var_id)
    product_name = variant.product
    # Format date and time to match format in cart
    date = variant.date.strftime('%B %d, %Y')
    time = variant.time.strftime('%H:%M')
    date_time = date + "/" + time
    # Loops through cart dict items
    # Loops through variant list for each item
    # If more than 1 variant, removes variant
    # If only 1 variant, removes product
    try:
        for product in cart:
            variants = cart.get(product)
            for var_instance in variants:
                if date_time in var_instance:
                    if len(variants) > 1:
                        variants.remove(var_instance)
                        request.session['cart'] = cart
                        messages.success(
                            request,
                            f"{product_name} for {date} at {time} "
                            "removed from your cart!"
                            )
                        raise StopIteration
                    else:
                        del cart[product]
                        request.session['cart'] = cart
                        messages.success(
                            request,
                            f"{product_name} for {date} at {time} "
                            "removed from your cart!"
                            )
                        raise StopIteration
    except StopIteration:
        pass
    except Exception as e:
        messages.error(request, "Error removing item, please try again.")
    return render(request, 'cart/cart.html')
