from datetime import datetime
import json
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from cart.contexts import cart_contents
import stripe
from products.models import Product, ProductVariant
from profiles.models import UserProfile
from .forms import Order, OrderForm
from .models import OrderLineItem


# @require_POST
# def cache_checkout_data(request):
#     """  Cache checkout data for saving customer info """
#     try:
#         pid = request.POST.get('client_secret').split('_secret')[0]
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         stripe.PaymentIntent.modify(pid, metadata={
#             'username': request.user,
#             'cart': json.dumps(request.sessions.get('cart')),
#         })
#         return HttpResponse(status=200)
#     except Exception as e:
#         messages.error(request, 'Sorry your payment cannot be processed \
#             right now. Please try again later.')
#         return HttpResponse(content=e, status=400)


def checkout(request):
    """ Main view for checkout page """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(cart)
            order.save()
            for item_id, variants in cart.items():
                try:
                    product = Product.objects.get(id=item_id)

                    for variant in variants:
                        split_variant = variant.rsplit("/")
                        date, time = split_variant[0],split_variant[1]
                        formatted_date = datetime.strptime(date, '%B %d, %Y')
                        formatted_time = datetime.strptime(time, '%H:%M')
                        variant_selected = get_object_or_404(
                            ProductVariant, date=formatted_date, time=formatted_time
                            )
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            product_variant=variant_selected,
                        )
                        order_line_item.save()
                        variant_selected.places_sold = variant_selected.places_sold + 1
                        variant_selected.save()
                        # Set paid member status to user is account_required product is purchased
                        if product.account_required:
                            profile = get_object_or_404(UserProfile, user=request.user)
                            profile.paid_member_from = formatted_date
                            profile.is_paid_member = True
                            profile.save()

                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found. "
                        "Please contact us for assistance.")
                    )
                    order.delete()
                    return redirect(reverse('cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was a problem with your form. '
                'Please confirm your details are correct.'
            )
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There is nothing in your cart right now.")
            return redirect(reverse('products'))

        current_cart = cart_contents(request)
        total = current_cart['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request,
            'Stripe public key missing. Dont forget to set it in your environment!'
            )

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """ Render page for successful checkouts. """

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

    messages.success(request, f'Order successfully created! \
        Your Order number is {order_number}. A confirmation email \
        will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout-success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
