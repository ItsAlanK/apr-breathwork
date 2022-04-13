import uuid
from django.db import models
from django.conf import settings
from django.db.models import Sum
from products.models import Product, ProductVariant
from profiles.models import UserProfile


class Order(models.Model):
    """ Model holding order info """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _create_order_number(self):
        """ Create random order number """

        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ Set total value for order, summing lineitem values """

        self.total = self.lineitems.aggregate(Sum('line_item_total'))['line_item_total__sum'] or 0
        if not self.total:
            self.total = 0
        self.save()

    def save(self, *args, **kwargs):
        """ Set order number and save if no order number is set """

        if not self.order_number:
            self.order_number = self._create_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """ Model for each item in order """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        null=False, blank=False, related_name='lineitems'
        )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        null=False, blank=False
        )
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE,
        null=False, blank=False
        )
    line_item_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False
        )

    def save(self, *args, **kwargs):
        """ Save line item total value """

        self.line_item_total = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Product {self.product.name} on order {self.order.order_number}'
