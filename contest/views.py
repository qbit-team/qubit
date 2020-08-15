from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Contest
from django.contrib import messages
from django.utils import timezone

separator = 10

def show_json(request, contest_id):
    contest = get_object_or_404(Contest, code=contest_id)
    if not request.user.is_superuser :
        raise Http404()
    users = contest.participants.all()
    return render(request, 'contest/show_json.html', {
        'users' : users
    })

def show(request, contest_id):
    contest = get_object_or_404(Contest, code=contest_id)
    if timezone.now() < contest.date_start and not request.user.is_superuser :
        raise Http404()
    problems = contest.problem_set.all()
    contest_problems = []
    if request.user.is_authenticated:
        for problem in problems:
            if problem.usertry(request.user):
                contest_problems.append((problem,problem.userscore(request.user)))
            else:
                contest_problems.append((problem,'-'))
    else:
        for problem in problems:
            contest_problems.append((problem,'-'))
    return render(request, 'contest/contest.html', {
        'contest' : contest ,
        'problems' : contest_problems ,
        'notifications':contest.notifications.all(),
    })

def scoreboard(request, contest_id):
    contest = get_object_or_404(Contest, code=contest_id)
    if timezone.now() < contest.date_start and not request.user.is_superuser :
        raise Http404()
    problems = contest.problem_set.all()
    users = contest.participants.all()
    l = []
    cms=0
    for p in problems:
        cms+=p.maxscore()
    for u in users:
        t = []
        ssc = 0
        for pp in problems:
            if pp.usertry(u):
                sf=pp.userscore(u)
                ssc+=sf
                t.append((sf,pp.maxscore))
            else:
                t.append(('-',pp.maxscore))
        l.append((ssc,u,t))
    l=sorted(l,key=lambda student:student[0], reverse=True) # sorted(student_tuples, key=lambda student: student[2]
    return render(request, 'contest/scorebord.html', {
        'contest' : contest ,
        'jadval' : l ,
        'problems' : problems ,
        'contest_maxscore': cms ,
    })

def page (request, page_number):
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

    if Contest.objects.filter(date_end__lt=timezone.now()).order_by('-date_start')[separator*(int(page_number)-1):separator*int(page_number)]:
        contests_history = Contest.objects.filter(date_end__lt=timezone.now()).order_by('-date_start')[separator*(int(page_number)-1):separator*int(page_number)]
    else:
        raise Http404()

    previous_contests = []
    for contest in contests_history:
        contest_duration = contest.date_end - contest.date_start
        if contest_duration.seconds//3600 > 24:
            days = (contest_duration.seconds//3600)//24
            hours = (contest_duration.seconds - days*3600)//3600
        else:
            days = 0
            hours = contest_duration.seconds//3600
            minutes = (contest_duration.seconds - hours*3600)//60
        previous_contests.append((contest,{"length_days":contest_duration.days,"length_hours":hours,"length_minutes":minutes}))

    return render(request, 'contest/contest_page.html', {
        'future_contests' : future_contests,
        'running_contests' : running_contests,
        'previous_contests' : previous_contests,
        'previous_page':str(int(page_number)-1),
        'next_page':str(int(page_number)+1),
        'current_page':str(int(page_number)),
        'last_page':str(int(len(Contest.objects.filter(date_end__lt=timezone.now()))/separator)+1),
    })
def index(request):
    return page(request, "1")
    #return HttpResponseRedirect("/contest/page/1/")

@login_required
def register_contest (request,contest_id):
    if request.method == "POST":
        contest = get_object_or_404(Contest, code=contest_id)
        if timezone.now()  < contest.date_start :
            if not contest.participants.filter(username = request.user.username):
                contest.participants.add(request.user)
                #messages.success(request, 'Registeration done!')
                return HttpResponseRedirect("/contest/page/1/")
            else:
                raise Http404()
        else:
            raise Http404()
    else:
        raise Http404()

@login_required
def register_contest_cancel (request,contest_id):
    if request.method == "POST":
        contest = get_object_or_404(Contest, code=contest_id)
        if timezone.now()  < contest.date_start :
            if contest.participants.filter(username = request.user.username):
                contest.participants.remove(request.user)
                #messages.success(request, 'Cancellation done!')
                return HttpResponseRedirect("/contest/page/1/")
            else:
                raise Http404()
        else:
            raise Http404()
    else:
        raise Http404()
