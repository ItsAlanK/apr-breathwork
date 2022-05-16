from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import AboutUs


def about(request):
    """ View which returns index page """

    about_us = get_object_or_404(AboutUs, pk=1)

    context = {
        'about_us': about_us,
    }
    template = 'info/about-us.html'
    return render(request, template, context)


def contact(request):
    """ View which returns index page """

    if request.method == 'POST':
        sender_name = request.POST.get('name', '')
        sender_email = request.POST.get('email')
        message = request.POST.get('message', '')
        email_subject = f'Message from {sender_name}'
        email_body = (
            'APR Breathworks Contact form has received a new message.\n'
            f'Message sent by {sender_name}, email address: {sender_email}.\n'
            f'Message: {message}')
        email_sender = settings.DEFAULT_FROM_EMAIL
        email_recipient = settings.DEFAULT_FROM_EMAIL

        send_mail(
            email_subject,
            email_body, email_sender,
            [email_recipient], fail_silently=False)

        messages.success(
            request, 'Your message was sent. '
            'We will be sure to get back to you soon!')
        return redirect(reverse('home'))

    template = 'info/contact-us.html'
    return render(request, template)
