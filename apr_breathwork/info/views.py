from django.shortcuts import render

def about(request):
    """ View which returns index page """
    return render(request, 'info/about-us.html')
