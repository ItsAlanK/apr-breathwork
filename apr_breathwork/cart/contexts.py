from datetime import datetime
from django.shortcuts import get_object_or_404
from products.models import Product, ProductVariant


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
        variants_selected = []

        for variant in variants:
            split_variant = variant.rsplit("/")
            date, time = split_variant[0],split_variant[1]
            formatted_date = datetime.strptime(date, '%B %d, %Y')
            formatted_time = datetime.strptime(time, '%H:%M')
            variant_selected = get_object_or_404(ProductVariant, date=formatted_date, time=formatted_time)
            dates += [date]
            times += [time]
            variants_selected += [variant_selected]

        cart_items.append({
            'item_id': item_id,
            'amount': amount,
            'product': product,
            'variants_selected': variants_selected,
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
