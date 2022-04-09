from django.shortcuts import render, redirect
from django.contrib import messages

def view_cart(request):
    """ View which returns cart contents page """
    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    """ Add selected product to the cart """

    date = request.POST.get('date')
    time = request.POST.get('time')
    variant = date + "," + time
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    # Checks if product is in cart already
    # then checks if same variant is in cart
    # if not adds new variant/product to cart
    if item_id in list(cart.keys()):
        if variant in cart[item_id]:
            messages.error(request, "This class is already your cart!")
        else:
            cart[item_id] += [variant]
    else:
        cart[item_id] = [variant]

    request.session['cart'] = cart
    return redirect(redirect_url)
