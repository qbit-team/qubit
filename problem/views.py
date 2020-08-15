from django.shortcuts import render, get_object_or_404
from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import User
from .models import Problem,Subtask,Submission
from problemset.models import Queue
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def problem_show(request, problem_id):
    problem = get_object_or_404(Problem, code=problem_id)
    if not problem.is_visible and not request.user.is_superuser :
        raise Http404()
    s = problem.subtask_set.all().order_by("code")
    l = []
    if request.user.is_authenticated:
        for ss in s:
            l.append((ss,ss.is_accepted(request.user)))
    else:
        for ss in s:
            l.append((ss,0))

    problem_solved = True
    if request.user.is_authenticated:
        for ss in s:
            if ss.is_accepted(request.user) == 0:
                problem_solved = False

    # Contest Conditions
    contest_state = None
    if timezone.now() < problem.parent_contest.date_start:
        contest_state = "B"
    elif timezone.now() > problem.parent_contest.date_end:
        contest_state = "C"
    else:
        contest_state = "O"

    if contest_state == "B" and not request.user.is_superuser :
        raise Http404()

    return render(request, 'problem/problem.html', {
        'problem' : problem ,
        'subtasks' : l ,
        'contest_state' : contest_state,
        'problem_solved': problem_solved
    })
@login_required
def problem_change (request, problem_id):
    if request.method == 'GET':
        raise Http404()
    if not request.user.is_authenticated and not problem.is_visible:
        raise Http404()
    problem = get_object_or_404(Problem, code=problem_id)
    new_problem_text_editor = request.POST.get("problem_text_editor")
    problem.text = new_problem_text_editor
    problem.save()
    return HttpResponseRedirect("/problem/"+problem_id+"/")

@login_required
def problem_submissions (request, problem_id):
    if not request.user.is_authenticated and not problem.is_visible:
        raise Http404()
    problem = get_object_or_404(Problem, code=problem_id)
    contest_state = None
    if timezone.now() < problem.parent_contest.date_start:
        contest_state = "B"
    elif timezone.now() > problem.parent_contest.date_end:
        contest_state = "C"
    else:
        contest_state = "O"
    if contest_state == "B" and not request.user.is_superuser :
        raise Http404()

    l = []
    for ss in problem.subtask_set.all():
        l.append((ss,ss.is_accepted(request.user)))

    submissions = []
    problem_solved = True
    for subtask in problem.subtask_set.all():

        if subtask.is_accepted(request.user) == 0:
            problem_solved = False

        for submission in Submission.objects.filter(task = subtask, user = request.user):
            submissions.append(submission)

    return render(request, 'problem/submissions.html', {
        'problem' : problem ,
        'subtasks':l,
        'contest_state' : contest_state,
        'problem_solved': problem_solved,
        'submissions' : sorted(submissions,key=lambda item:item.release_date, reverse=True),
    })

@login_required
def problem_submit(request, problem_id):
    if request.method == 'GET':
        raise Http404()
    if not request.user.is_authenticated and not problem.is_visible:
        raise Http404()

    problem = get_object_or_404(Problem, code=problem_id)
    task = get_object_or_404(Subtask, code=request.POST.get("subtask-select"),problem=problem)

    contest_state = None
    if timezone.now() < problem.parent_contest.date_start:
        contest_state = "B"
    elif timezone.now() > problem.parent_contest.date_end:
        contest_state = "C"
    else:
        contest_state = "O"
    if contest_state == "B" and not request.user.is_superuser :
        raise Http404()

    sub = Submission()
    sub.user=request.user
    sub.task=task

    if request.POST.get('javab')==task.answer:
        sub.verdict=1
        sub.context = request.POST.get('javab')
        messages.success(request, 'Accepted!')
    else:
        sub.verdict=0
        sub.context = request.POST.get('javab')
        messages.error(request, 'Wrong answer.')
    sub.save()
    return HttpResponseRedirect("/problem/"+task.problem.code)

@login_required
def coq_show(request, problem_id):
    problem = get_object_or_404(Problem, code=problem_id)
    if not problem.is_visible and not request.user.is_superuser :
        raise Http404()
    s = problem.subtask_set.all().order_by("code")
    l = []
    hasCoq = False

    for ss in s:
        if ss.style=="coq":
            hasCoq = True
        l.append((ss,ss.is_accepted(request.user)))

    if not hasCoq:
        raise Http404()

    problem_solved = True
    if request.user.is_authenticated:
        for ss in s:
            if ss.is_accepted(request.user) == 0:
                problem_solved = False

    # Contest Conditions
    contest_state = None
    if timezone.now() < problem.parent_contest.date_start:
        contest_state = "B"
    elif timezone.now() > problem.parent_contest.date_end:
        contest_state = "C"
    else:
        contest_state = "O"

    if contest_state == "B" and not request.user.is_superuser :
        raise Http404()

    return render(request, 'problem/submit.html', {
        'problem' : problem ,
        'subtasks' : l ,
        'contest_state' : contest_state,
        'problem_solved': problem_solved
    })
@login_required
def show_submission (request, problem_id, submission_id):
    sub = get_object_or_404(Submission, id=submission_id)
    if sub.user == request.user or request.user.is_superuser:
        return render(request, 'problem/submission.html', {
        'submission':sub,
        })
    else:
        raise Http404()
@login_required
def coq_submit(request, problem_id):
    if request.method == 'GET':
        raise Http404()
    if not request.user.is_authenticated and not problem.is_visible:
        raise Http404()

    problem = get_object_or_404(Problem, code=problem_id)
    task = get_object_or_404(Subtask, code=request.POST.get("subtask-select"),problem=problem)

    contest_state = None
    if timezone.now() < problem.parent_contest.date_start:
        contest_state = "B"
    elif timezone.now() > problem.parent_contest.date_end:
        contest_state = "C"
    else:
        contest_state = "O"
    if contest_state == "B" and not request.user.is_superuser :
        raise Http404()

    sub = Submission()
    sub.user = request.user
    sub.task = task
    sub.context = request.POST.get('javab')
    sub.verdict = 2 # 2 -> in queue # 3 -> under judge
    sub.save()
    queueObj = Queue()
    queueObj.user = request.user
    queueObj.task = task
    queueObj.submission = sub
    queueObj.save()
    messages.success(request, 'Submission now in judge queue!')
    return HttpResponseRedirect("/problem/"+task.problem.code)

