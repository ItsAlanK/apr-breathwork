from django.shortcuts import render, get_object_or_404
from .models import AboutUs

def about(request):
    """ View which returns index page """

    about_us = get_object_or_404(AboutUs, pk=1)

    context = {
        'about_us': about_us,
    }
    template = 'info/about-us.html'
    return render(request, template, context)
