from django.shortcuts import render, redirect

def view_cart(request):
    """ View which returns cart contents page """
    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    """ Add selected product to the cart """

    date = request.POST.get('date')
    time = request.POST.get('time')
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        print('item already in bag')
    else:
        cart[item_id] = date + time

    request.session['cart'] = cart
    print(request.session['cart'])
    return redirect(redirect_url)
