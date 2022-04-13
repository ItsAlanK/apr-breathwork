from django.shortcuts import render, get_object_or_404
from checkout.models import Order
from .models import UserProfile
from django.contrib import messages



def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'orders': orders,
    }


    return render(request, template, context)


def order_history(request, order_number):
    """ Order history view """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout-success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
