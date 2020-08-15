from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import auth_login
from django.contrib.auth.decorators import login_required
from django.http import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.utils import timezone
from django.utils import dateformat
from django.conf import settings
from .models import Mail
import requests
import secrets

sep = 20

@login_required
def inbox (request, page_number):
    if request.is_secure:
        if request.user.is_superuser:
            mails = Mail.objects.filter(is_reply=False, receiver=request.user).order_by('-id')[sep*(int(page_number)-1):sep*int(page_number)]
            return render(request, 'mail/inbox.html', {
                "mails":mails,
                })
        else:
            return HttpResponse("Page is available but you don't have sufficient permissions to enter.")
    else:
        return HttpResponseForbidden()

@login_required
def view_mail (request, mail_id):
    if request.is_secure:
        if request.user.is_superuser:
            return HttpResponse("Mail Id.")
        else:
            return HttpResponse("Page is available but you don't have sufficient permissions to enter.")
    else:
        return HttpResponseForbidden()

@login_required
def view_inbox_first_page (request):
    if request.is_secure:
        if request.user.is_superuser:
            return inbox(request, 1)
        else:
            return HttpResponse("Page is available but you don't have sufficient permissions to enter.")
    else:
        return HttpResponseForbidden()

@login_required
def compose_mail (request):
    if request.is_secure:
        if request.user.is_superuser:
            if request.method == "POST":
                pass
            else:
                superusers = User.objects.filter(is_superuser = True)
                return render(request, 'mail/compose.html', {
                    "superusers":superusers,
                    })
        else:
            return HttpResponse("Page is available but you don't have sufficient permissions to enter.")
    else:
        return HttpResponseForbidden()

@login_required
def sents (request):
    if request.is_secure:
        if request.user.is_superuser:
            return HttpResponse("Sents.")
        else:
            return HttpResponse("Page is available but you don't have sufficient permissions to enter.")
    else:
        return HttpResponseForbidden()

@login_required
def drafts (request):
    if request.is_secure:
        if request.user.is_superuser:
            return HttpResponse("Drafts.")
        else:
            return HttpResponse("Page is available but you don't have sufficient permissions to enter.")
    else:
        return HttpResponseForbidden()