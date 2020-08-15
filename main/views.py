# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Profile, email_token, password_token
from django.contrib.auth.views import auth_login
from django.contrib.auth.decorators import login_required
from django.http import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from .forms import UploadFileForm
from problem.models import Submission
from contest.models import Contest
from django.utils import timezone
from django.utils import dateformat
import requests
import random
from django.conf import settings
import secrets
from .EmailTemplates import *

separator = 15
def index(request):
    return HttpResponseRedirect("/blog")
    #return render(request, 'main/index.html')
def isEnglish (s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
def handler_error_404 (request):
    return render(request, 'main/404.html')
def handler_error_500 (request):
    return render(request, 'main/500.html')
def validate_username (username):
    if isEnglish(username):
        out = True
        for char in username:
            if 97 <= ord(char) <= 122 : # a
                continue
            elif 65 <= ord(char)<= 90 : # A
                continue
            elif 48 <= ord(char) <= 57: # digit
                continue
            elif ord(char) == 95: # _
                continue
            elif ord(char) == 45: # -
                continue
            elif ord(char) == 46: # .
                continue
            else:
                return False
        return True
    else:
        return False

"""
def make_verify(request):
    for p in Profile.objects.filter(email_verified=False):
        if not p.user.is_superuser:
            u = User.objects.get(username = p.user.username)
            u.is_active=False
            u.save()
            t = email_token(user = p.user, token = secrets.token_urlsafe(50), used=False)
            t.save()
            send_mail("Accounts Activation","",settings.EMAIL_HOST_USER,[p.user.email], fail_silently=False, html_message=email_template.format(p.user.first_name,t.token))
    return HttpResponseRedirect("Emails Sent!")
"""
"""
def verify_test(request):
    send_mail("کیوبیت - فعال سازی حساب کاربری",
    "",settings.EMAIL_HOST_USER,["a.h.rajabi@outlook.com"], fail_silently=False, html_message=new_account_template("237","amirhosein as admin"))
    return render(request, 'main/verify.html',
    {'verification_before':True
    })
    return HttpResponse("Automatic Email System Test Passed SUCCESSFULLY")
"""
def register(request):
    if not request.user.is_authenticated :
        if request.method=="POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            password_confirmation = request.POST.get("password_confirmation")
            email = request.POST.get("email")
            try:
                validate_email(email)
                pass
            except:
                return render(request, 'main/register.html',{'email_error':True})
            if not validate_username (username):
                return render(request, 'main/register.html',{'username_error':True})
            if len(username) > 150:
                return render(request, 'main/register.html',{'username_error':True})
            firstname = request.POST.get("firstname")
            organization = request.POST.get("organization")
            if password != password_confirmation:
                return render(request, 'main/register.html',{'conf_error':True})
            if username == "" or password == "" or password_confirmation == "" or email =="" or firstname == "" or organization=="":
                return render(request, 'main/register.html',{'fill_error':True})
            if len(User.objects.filter(email=email)) > 0:
                return render(request, 'main/register.html',{'email_exist_error':True})
            if len(User.objects.filter(username=username)) > 0:
                return render(request, 'main/register.html',{'user_error':True})
            #try:
            avatars = ["default/solid-blue.jpg","default/solid-green.jpg","default/solid-orange.jpg","default/solid-red.jpg"]
            newUser = User.objects.create_user(username,email,password,is_active=False)
            newUser.first_name = firstname
            newUser.email = email
            newUser.save()
            newUser.profile.origin = organization
            newUser.profile.last_active = timezone.now()
            newUser.profile.photo = random.choice(avatars)
            newUser.profile.save()
            t = email_token(user = newUser, token = secrets.token_urlsafe(50), used=False, email=email + " (USER IS REGISTERING IN QUBIT SYSTEM)")
            t.save()
            try:
                send_mail("کیوبیت - فعال سازی حساب کاربری",
                "",settings.EMAIL_HOST_USER,[email], fail_silently=False, html_message=new_account_template(t.token,firstname))
                return render(request, 'main/verify.html',
                {'verification_before':True
                })
            except:
                return HttpResponse("Sending-Email failed. Please contact with contact.qbit@gmail.com to recieve verification code manually. This is a server error. We apologize for this.")
            #login(request,authenticate(username=username, password=password))
            #if request.POST.get("next") != None :
            #    return HttpResponseRedirect(request.POST.get("next"))
            #else:
            #    return HttpResponseRedirect("/")
            #except:
            #    return render(request, 'main/register.html',{'user_error':True})
        else:
            return render(request, 'main/register.html',{'next':request.GET.get("next")})
    else:
        return HttpResponseRedirect("/accounts/logout/?next=/accounts/register/")
def reset_password (request, token):
    from .models import password_token
    p_t = get_object_or_404(password_token,token=token, used=False, expiration__gt = timezone.now())
    if request.method == "POST":
        if token != request.POST.get("who"):
            return HttpResponseForbidden()
        if request.POST.get("password") != request.POST.get("password_confirm"):
            return render(request, 'main/reset.html',
            {'MATCH':True, 'firstname': p_t.user.first_name
            })
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            c_ip = x_forwarded_for.split(',')[0]
        else:
            c_ip = request.META.get('REMOTE_ADDR')
        password_token = get_object_or_404(password_token,token=request.POST.get("who"), used=False, expiration__gt = timezone.now())
        password_token.user.set_password(request.POST.get("password"))
        password_token.user.save()
        password_token.used = True
        password_token.release_changer = timezone.now()
        password_token.client_ip_changer = c_ip
        password_token.client_info_changer = request.META['HTTP_USER_AGENT']
        password_token.save()
        try:
            send_mail("کیوبیت - رمز عبور شما تغییر کرد",
            "",settings.EMAIL_HOST_USER,[password_token.user.email], fail_silently=False, html_message=password_changed_template(password_token.user.first_name,c_ip,str(dateformat.format(timezone.now(), 'F j, Y, P'))))
            return render(request, 'main/verify.html',
            {'verification_password_after':True,
            })
        except:
            return HttpResponse("Your password was reset. Please contact with contact.qbit@gmail.com if there is any problem leftover.")

    else:
        return render(request, 'main/reset.html',
        {'aim_token':token, 'firstname': p_t.user.first_name
        })

def forget_password (request):
    #return HttpResponse("Page under construction!")
    if request.method == "POST":
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            c_ip = x_forwarded_for.split(',')[0]
        else:
            c_ip = request.META.get('REMOTE_ADDR')
        if request.POST.get("email") != "":
            try:
                user = get_object_or_404(User,email=request.POST.get("email"))
            except:
                return render(request, 'main/forget.html',{"EMAIL_EXIST_ERROR":True})
            t_expire = timezone.now() + timezone.timedelta(days=1)
            t = password_token(user = user, token = secrets.token_urlsafe(50), used=False,client_ip = c_ip, client_info=request.META['HTTP_USER_AGENT'],expiration=t_expire)
            t.save()
            try:
                send_mail("کیوبیت - تغییر رمز عبور",
                "",settings.EMAIL_HOST_USER,[user.email], fail_silently=False, html_message=password_reset_template(t.token,user.first_name,str(request.META['HTTP_USER_AGENT']),c_ip,str(dateformat.format(timezone.now(), 'F j, Y, P'))))
                return render(request, 'main/verify.html',
                {'verification_password_before':True
                })
            except:
                return HttpResponse("Your password token has been generated successfully but we could not send an email with the password reset link in it. Maybe our mail server has stopped working. Please contact 'contact.qbit@gmail.com' to get help and reset your password. We apologize for this discomfort.")

        else:
            return render(request, 'main/forget.html',{"FILL_ERROR":True})
    else:
        return render(request, 'main/forget.html')

def profile (request, username):
    user = get_object_or_404(User,username=username)
    profile = get_object_or_404(Profile,user=user)
    return render(request, 'main/profile.html',
    {
        "profile":profile,
        "contests_in": user.contest_set.all(),
        "server_time": timezone.now(),
    })
@login_required
def settings_personal (request):
    return render(request, 'main/dashboard.html',
    {'personal_settings':True,
     'profile': Profile.objects.get(user=request.user)
    })
@login_required
def settings_password (request):
    return render(request, 'main/dashboard.html',
    {'password_settings':True,
    })
@login_required
def settings_email (request):
    return render(request, 'main/dashboard.html',
    {'email_settings':True,
    'profile': Profile.objects.get(user=request.user),
    })
@login_required
def change_profile (request):
    if request.method == "POST":
        if request.POST.get("first_name") != "" and request.POST.get("organization") != "":
            p = Profile.objects.get(user=request.user)
            p.origin = request.POST.get("organization")
            p.save()
            u = User.objects.get(username=request.user.username)
            u.first_name= request.POST.get("first_name")
            u.save()
            messages.success(request, 'Done!')
            return HttpResponseRedirect("/accounts/settings/personal/")
    else:
        raise Http404()
    return render(request, 'main/dashboard.html',
    {'personal_settings':True,
     'profile': Profile.objects.get(user=request.user)
    })
@login_required
def change_email_pref (request):
    if request.method == "POST":
        p = Profile.objects.get(user=request.user)
        if request.POST.get("EmailForNews") == "on":
            p.email_for_news = True
        if request.POST.get("EmailForNews") == None:
            p.email_for_news = False
        if request.POST.get("EmailForContest") == "on":
            p.email_for_contest = True
        if request.POST.get("EmailForContest") == None:
            p.email_for_contest = False
        p.save()
        messages.success(request, 'Done!')
        return HttpResponseRedirect("/accounts/settings/email/")
    else:
        raise Http404()
@login_required
def change_email (request):
    if request.method == "POST":
        if request.POST.get("email") != "":
            try:
                validate_email(request.POST.get("email"))
            except:
                return render(request, 'main/dashboard.html',{'email_settings_error':True,'email_settings':True})
            if request.POST.get("email") == request.user.email:
                return render(request, 'main/dashboard.html',{'email_settings':True})
            else:
                if len(User.objects.filter(email=request.POST.get("email"))) > 0:
                    return render(request, 'main/dashboard.html',{'email_settings_error':True,'email_settings':True})
                p = Profile.objects.get(user=request.user)
                u = User.objects.get(username = request.user.username)
                t = email_token(user = request.user, token = secrets.token_urlsafe(50), email = "New email address is going to be: '" + request.POST.get("email") + "' Current email address is: '" + u.email + "'", used=False)
                t.save()
                try:
                    send_mail("کیوبیت - فعال سازی حساب کاربری",
                    "",settings.EMAIL_HOST_USER,[request.POST.get("email")], fail_silently=False, html_message=activation_template(t.token,request.user.first_name))
                    send_mail("کیوبیت - ایمیل شما تغییر کرد.",
                    "",settings.EMAIL_HOST_USER,[u.email], fail_silently=False, html_message=email_change_done_template(request.user.first_name,u.email,request.POST.get("email")))
                except:
                    return HttpResponse("We could not send you an email with your new email verification link in it. Your email has not changed yet but your email token is ready. Please contact contact.qbit@gmail.com to get help.")
                p.email_verified = False
                u.email = request.POST.get("email")
                u.is_active = False
                u.save()
                p.save()
                return render(request, 'main/verify.html',
                {'verification_again':True
                })
    else:
        raise Http404()
def verify_accounts(request, token):
    url = get_object_or_404(email_token, token=token, used=False)
    url.used=True
    url.save()
    p = Profile.objects.get(user=url.user)
    p.email_verified = True
    p.save()
    u = User.objects.get(username = url.user.username)
    u.is_active = True
    u.save()
    try:
        send_mail("کیوبیت - حساب کاربری شما فعال شد",
        "",settings.EMAIL_HOST_USER,[u.email], fail_silently=False, html_message=activation_done_template(u.first_name,u.email))
        #login(request,authenticate(username=u.username, password=u.password))
    except:
        pass
    return render(request, 'main/verify.html',
    {'verification_done':True
    })
@login_required
def show_contests (request, page_number):
    all_contests = Contest.objects.all()
    list_contests = []
    for contest in all_contests :
        if contest.participants.filter(username = request.user.username):
            contest_duration = contest.date_end - contest.date_start
            if contest_duration.seconds//3600 > 24:
                days = (contest_duration.seconds//3600)//24
                hours = (contest_duration.seconds - days*3600)//3600
            else:
                days = 0
                hours = contest_duration.seconds//3600
                minutes = (contest_duration.seconds - hours*3600)//60
            list_contests.append((contest,{"length_days":contest_duration.days,"length_hours":hours,"length_minutes":minutes}))
    if len(list_contests[separator*(int(page_number)-1):separator*int(page_number)]) == 0:
        return render(request, 'main/dashboard.html',
        {'contests_settings':True,
        })
        raise Http404()
    return render(request, 'main/dashboard.html',
    {'contests_settings':True,
    'contests': sorted(list_contests,key=lambda item:item[0].date_start, reverse=True)[separator*(int(page_number)-1):separator*int(page_number)],
    'previous_page':str(int(page_number)-1),
    'next_page':str(int(page_number)+1),
    'current_page':str(int(page_number)),
    'last_page':str(int(len(list_contests)/separator)+1),
    })
@login_required
def show_submissions (request, page_number):
    submissions = Submission.objects.filter(user=request.user).order_by('-release_date')[separator*(int(page_number)-1):separator*int(page_number)]
    if len(submissions) == 0:
        return render(request, 'main/dashboard.html',
        {'submissions_settings':True,
        })
    return render(request, 'main/dashboard.html',
    {'submissions_settings':True,
     'submissions': submissions,
    'previous_page':str(int(page_number)-1),
    'next_page':str(int(page_number)+1),
    'current_page':str(int(page_number)),
    'last_page':str(int(len(Submission.objects.filter(user=request.user))/separator)+1),
    })
@login_required
def change_password (request):
    if request.method == "POST":
        if request.POST.get("old_password") != "" and request.POST.get("new_password") != "" and request.POST.get("new_password_confirm") != "":
            user = User.objects.get(username = request.user.username)
            if not user.check_password(request.POST.get("old_password")):
                #messages.error(request, "OLD")
                return render(request, 'main/dashboard.html',
                {'password_settings':True,
                 'old_password_error':True,
                })
            if not request.POST.get("new_password") == request.POST.get("new_password_confirm"):
                #messages.error(request, "MATCH")
                return render(request, 'main/dashboard.html',
                {'password_settings':True,
                 'match_password_error':True,
                })
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                c_ip = x_forwarded_for.split(',')[0]
            else:
                c_ip = request.META.get('REMOTE_ADDR')
            user.set_password(request.POST.get("new_password"))
            user.save()
            try:
                send_mail("کیوبیت - رمز عبور شما تغییر کرد",
                "",settings.EMAIL_HOST_USER,[request.user.email], fail_silently=False, html_message=password_changed_template(request.user.first_name,c_ip,str(dateformat.format(timezone.now(), 'F j, Y, P'))))
            except:
                pass
            messages.success(request, 'Done!')
            return HttpResponseRedirect("/accounts/settings/password/")
    else:
        raise Http404()
def change_profile_photo (request):
    if request.method == "POST":
        try:
            if request.FILES['profile_photo_file']._size > 1200000:
                #messages.error(request, 'FILE')
                #return HttpResponseRedirect("/accounts/settings/personal/")
                return render(request, 'main/dashboard.html',
                {'personal_settings':True,
                 'file_size_error':True,
                })
            filename = request.FILES['profile_photo_file']._name
            if not filename.split(".")[len(filename.split("."))-1] in ["jpg","JPEG","png","PNG","bmp","BMP"]:
                return HttpResponseRedirect("/accounts/settings/personal/")
            p = Profile.objects.get(user = request.user)
            p.photo = request.FILES['profile_photo_file']
            p.save()
            messages.success(request, 'Done!')
            return HttpResponseRedirect("/accounts/settings/personal/")
        except:
            return HttpResponseRedirect("/accounts/settings/personal/")
    else:
        raise Http404()
