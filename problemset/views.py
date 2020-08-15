from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.http import *
from django.contrib.auth.models import User
from contest.models import Contest,Problem
from django.utils import timezone
from .models import Queue

separator = 15

def page(request, page_number):
    ########################## Contests
    if Contest.objects.filter(date_start__gt=timezone.now()) or Contest.objects.filter(date_start__lt=timezone.now(), date_end__gt=timezone.now()) :
        if Contest.objects.filter(date_start__gt=timezone.now()): # before contest
            future_contests_pack = Contest.objects.filter(date_start__gt=timezone.now())
            future_contests = []
            for contest in future_contests_pack:
                contest_duration = contest.date_end - contest.date_start
                if contest_duration.seconds//3600 > 24:
                    days = (contest_duration.seconds//3600)//24
                    hours = (contest_duration.seconds - days*3600)//3600
                else:
                    days = 0
                    hours = contest_duration.seconds//3600
                    minutes = (contest_duration.seconds - hours*3600)//60
                if contest.date_start < timezone.now():
                    registration_closed = True
                else:
                    registration_closed = False
                if contest.participants.filter(username = request.user.username):
                    has_registered = True
                else:
                    has_registered = False
                future_contests.append((contest,{"length_days":contest_duration.days,"length_hours":hours,"length_minutes":minutes,"registration_closed":registration_closed, "has_registered":has_registered}))
        else:
            future_contests = None
        if Contest.objects.filter(date_start__lt=timezone.now(), date_end__gt=timezone.now()): # during contest
            running_contests_pack = Contest.objects.filter(date_start__lt=timezone.now(), date_end__gt=timezone.now())
            running_contests = []
            for contest in running_contests_pack:
                contest_duration = contest.date_end - contest.date_start
                if contest_duration.seconds//3600 > 24:
                    days = (contest_duration.seconds//3600)//24
                    hours = (contest_duration.seconds - days*3600)//3600
                else:
                    days = 0
                    hours = contest_duration.seconds//3600
                    minutes = (contest_duration.seconds - hours*3600)//60
                if contest.participants.filter(username = request.user.username):
                    has_registered = True
                else:
                    has_registered = False
                running_contests.append((contest,{"length_days":contest_duration.days,"length_hours":hours,"length_minutes":minutes, "has_registered":has_registered}))
        else:
            running_contests = None
    else:
        future_contests = None
        running_contests = None
    ###################################################### Main
    if not Problem.objects.filter(is_visible = True).order_by('-id')[separator*(int(page_number)-1):separator*int(page_number)]:
        raise Http404()
    problems = Problem.objects.filter(is_visible = True).order_by('-id')[separator*(int(page_number)-1):separator*int(page_number)]
    conditional_problems = []
    all_conditional_problems = []
    for problem in Problem.objects.filter(is_visible = True) :
        if not timezone.now() < problem.parent_contest.date_start :
            all_conditional_problems.append(problem)
    for problem in problems :
        if not timezone.now() < problem.parent_contest.date_start :
            conditional_problems.append(problem)
    l = []
    if request.user.is_authenticated:
        for problem in conditional_problems :
            if problem.usertry(request.user):
                l.append((problem,problem.userscore(request.user)))
            else:
                l.append((problem,'-'))
    else:
        for problem in conditional_problems :
            l.append((problem,'-'))
    #################################################### Search
    return render(request, 'problemset/problemset.html', {
        'future_contests' : future_contests,
        'running_contests' : running_contests,
        'problems' : l ,
        'previous_page':str(int(page_number)-1),
        'next_page':str(int(page_number)+1),
        'current_page':str(int(page_number)),
        'last_page':str(int(len(all_conditional_problems)/separator)+1),
        'all_problems':all_conditional_problems,
    })
def queue (request):
    return render(request, 'problemset/queue.html', {
        'submissions':Queue.objects.filter(is_judged=False).order_by('-id'),
    })
def index(request):
    return page(request, "1")