from django.http import HttpResponse


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
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_failed(self, event):
        """ Handle failed payment intent webhook events """

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
