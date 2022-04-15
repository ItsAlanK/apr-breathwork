from django.shortcuts import render, get_object_or_404
from checkout.models import Order
from .models import UserProfile
from django.contrib import messages



def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    course_name = ''
    membership_from = ''

    orders = profile.orders.all()
    if profile.is_paid_member:
        for order in orders:
            items = order.lineitems.all()
            for item in items:
                if item.product.account_required:
                    course_name = item.product.name
                    membership_from = item.product_variant.date

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'orders': orders,
        'course_name': course_name,
        'membership_from': membership_from,
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
