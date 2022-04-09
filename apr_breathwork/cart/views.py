from django.shortcuts import render

def view_cart(request):
    """ View which returns cart contents page """
    return render(request, 'cart/cart.html')
