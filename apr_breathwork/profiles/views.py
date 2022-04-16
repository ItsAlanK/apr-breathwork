from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order
from course.models import CourseInfo
from .models import UserProfile


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    course_name = []
    membership_from = []
    course_id = []
    course_details = zip(course_name, membership_from, course_id)
    course_exists = False
    course_ready = True

    orders = profile.orders.all()
    try:
        if profile.is_paid_member:
            # for each order in users order history
            for order in orders:
                items = order.lineitems.all()
                # for each line item in each order
                for item in items:
                    # if line item is a course (acc required)
                    if item.product.account_required:
                        course_exists = True
                        course_name += [item.product.name]
                        course = CourseInfo.objects.get(course=item.product)
                        course_id += [course.pk]
                        membership_from += [item.product_variant.date]
    except:
        course_ready = False

    # If user somehow gets is_paid_member set to true without
    # buying a course this resets to false to stop empty
    # course membership section in template.
    if not course_exists:
        profile.is_paid_member=False
        profile.save()

    template = 'profiles/profile.html'
    context = {
        'profile': profile,
        'orders': orders,
        'course_details': course_details,
        'course_ready': course_ready,
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
