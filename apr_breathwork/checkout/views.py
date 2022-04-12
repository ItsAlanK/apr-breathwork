from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    """ Main view for checkout page """
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There is nothing in your cart right now.")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51KneNXCIed9b14TmGqTxd3a40nBZZE7mmpNoZUBKbuEq2fLafbou69kJUj0PWUnVLUiG2Ft4lmexSopMUaBheElx00bHBrgR8k',
        'client_secret': 'test_client_secret',
    }

    return render(request, template, context)
