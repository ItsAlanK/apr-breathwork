from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from profiles.models import UserProfile
from checkout.models import Order, OrderLineItem
from products.models import Product, ProductVariant
from .models import CourseInfo, Urls


def course_page(request, course_id):

    """ View which returns detailed view of the requested product """

    course_info = get_object_or_404(CourseInfo, pk=course_id)
    classes = Urls.objects.filter(course=course_info)
    product = get_object_or_404(Product, course=course_info)
    variant = get_object_or_404(ProductVariant, product=product)
    purchases = []

    context = {
            'course_info': course_info,
            'classes': classes,
        }
    if request.user.is_authenticated:
        requester = get_object_or_404(UserProfile, user=request.user)
        if requester.is_paid_member:
            past_orders = Order.objects.filter(user_profile=requester)
            for order in past_orders:
                line_items = OrderLineItem.objects.filter(order=order)
                for item in line_items:
                    purchases.append(item.product_variant)
                    print(purchases)
            if variant in purchases:
                return render(request, 'course/course.html', context)
            else:
                messages.error(
                    request, 'Oops, you must purchase this course '
                    'to view its content.')
                return redirect(f'/products/{product.id}')
        else:
            messages.error(
                request, 'Oops, you must purchase this course '
                'to view its content.')
            return redirect(f'/products/{product.id}')
    else:
        messages.error(
            request, 'Oops, if you have purchased this course '
            'please log in to your account to view its content. Otherwise '
            'create an account and purchase the course.'
            )
        return redirect(f'/products/{product.id}')
