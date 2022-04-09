from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """ Context processor makes cart contents available across site """

    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    product_count = 0

    for item_id, variants in cart.items():
        product = get_object_or_404(Product, pk=item_id)
        amount = len(variants)
        subtotal = product.price * amount
        total += product.price * amount
        dates = []
        times = []

        for variant in variants:
            split_variant = variant.rsplit("/")
            date, time = split_variant[0],split_variant[1]
            dates += [date]
            times += [time]

        cart_items.append({
            'item_id': item_id,
            'amount': amount,
            'product': product,
            'variants': variants,
            'dates': dates,
            'times': times,
            'subtotal': subtotal,
        })

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
    }

    return context
