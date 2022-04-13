from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """ Set OrderLineItem admin to be visible from Order Admin """

    model = OrderLineItem
    readonly_fields = ('line_item_total',)
    fields = (
        'product', 'product_variant',
        'line_item_total',
        )


class OrderAdmin(admin.ModelAdmin):
    """ Admin settings for Order model """

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date', 'total',)

    fields = (
        'order_number', 'user_profile',
        'date', 'full_name', 'email',
        'phone_number', 'total',
        )

    list_display = (
        'order_number', 'date',
        'full_name', 'total'
        )

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)
