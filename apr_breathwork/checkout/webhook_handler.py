from datetime import datetime
import json
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from products.models import Product, ProductVariant
from profiles.models import UserProfile
from .models import Order, OrderLineItem


class StripeWebhookHandler:
    """ Handle stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Handle generic/unexpected/unknown webhook events """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """ Handle successful payment intent webhook events """

        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart

        billing_details = intent.charges.data[0].billing_details
        total = round(intent.charges.data[0].amount / 100, 2)

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=billing_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=billing_details.phone,
                    total=total,
                    original_bag=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                datetime.time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]}',
                status=200
            )
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    original_bag=cart,
                    stripe_pid=pid,
                )
                for item_id, variants in json.loads('cart').items():
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
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}'
                    )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Order already exists in db',
            status=200
        )


    def handle_payment_intent_failed(self, event):
        """ Handle failed payment intent webhook events """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
