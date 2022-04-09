from django.shortcuts import render, redirect

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

    if item_id in list(cart.keys()):
        if variant in cart[item_id]:
            print("Already in cart")
        else:
            cart[item_id] += [variant]
    else:
        cart[item_id] = [variant]

    request.session['cart'] = cart
    print(request.session['cart'])
    return redirect(redirect_url)
