from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages

from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


# Subscription Logic
def subscribe(email):
    """
     Contains code handling the communication to the mailchimp api
     to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        return True
    except ApiClientError as error:
        return False


def index(request):
    """ View which returns index page and handles Mailchimp subscription form in footer """

    if request.method == "POST":
        email = request.POST['email']
        submission = subscribe(email)
        redirect_url = request.POST.get('next', '/')
        if submission:
            messages.success(request, "Email received. Thanks for subscribing! ")
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, "Please ensure you use are using a valid email and try again")
            return HttpResponseRedirect(redirect_url)
    else:
        return render(request, 'home/index.html')


def page_not_found_handler(request, exception):
    """ Render 404 page """
    return render(request, 'home/404.html')
