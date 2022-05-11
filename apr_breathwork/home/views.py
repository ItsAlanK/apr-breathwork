from django.shortcuts import render

def index(request):
    """ View which returns index page """
    return render(request, 'home/index.html')


def page_not_found_handler(request, exception):
    """ Render 404 page """
    return render(request, 'home/404.html')
