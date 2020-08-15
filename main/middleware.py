from django.http import *
from django.conf import settings
from django.shortcuts import redirect
from .models import Profile
from django.utils import timezone
import requests, os

class RobotSecurity(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.method == "POST":

            if request.POST.get("g-recaptcha-response") != None and request.POST.get("authentication_recaptcha") == "1": #if request.get_full_path() == "/accounts/login/" or request.get_full_path() == "/accounts/register/":
                #if request.POST.get("g-recaptcha-response")!= None and request.POST.get("g-recaptcha-response")!= "":
                google_response = request.POST.get("g-recaptcha-response")
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                params = {
                    'secret': settings.RECAPTCHA_AUTH_SECRET,
                    'response': google_response,
                    'remoteip': ip,

                }
                r = requests.get(url, params=params)
                answer = r.json()
                if answer["success"] == True:
                    pass
                else:
                    return HttpResponseForbidden()
            if request.POST.get("g-recaptcha-response") != None and request.POST.get("submission_recaptcha") == "1": #if request.get_full_path() == "/accounts/login/" or request.get_full_path() == "/accounts/register/":
                #if request.POST.get("g-recaptcha-response")!= None and request.POST.get("g-recaptcha-response")!= "":
                google_response = request.POST.get("g-recaptcha-response")
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                params = {
                    'secret': settings.RECAPTCHA_SUBMISSION_SECRET,
                    'response': google_response,
                    'remoteip': ip,

                }
                r = requests.get(url, params=params)
                answer = r.json()
                if answer["success"] == True:
                    pass
                else:
                    return HttpResponse("You are BOT!")



        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
class UserState (object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        if request.user.is_authenticated:
            p = Profile.objects.get(user=request.user)
            p.last_active = timezone.now()
            p.save()

        response = self.get_response(request)

        return response