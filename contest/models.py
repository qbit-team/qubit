from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from problem.models import Problem
from django.utils import timezone
from django.template import loader

# Create your models here.

class Notification (models.Model):
    title = models.CharField(max_length=400)
    author = models.ForeignKey(User)
    context = models.TextField(blank=True)
    code = models.CharField(max_length=400)
    release = models.DateTimeField(auto_now_add=True)
    seen = models.ManyToManyField(User,blank=True,related_name="seens")
    conditions = models.TextField(blank=True)
    def __str__(self):
        return self.code

class Contest(models.Model):
    problems = models.ManyToManyField(Problem, blank=True)
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=400)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    pc = models.TextField(blank=True)
    participants = models.ManyToManyField(User,blank=True)
    notifications = models.ManyToManyField(Notification ,blank=True)
    def __str__(self):
        return self.code
    def html_div(self):
        template = loader.get_template('contest/contest_div.html')
        contest_state = None
        if timezone.now() < self.date_start:
            contest_state = "B"
        elif timezone.now() > self.date_end:
            contest_state = "C"
        else:
            contest_state = self.date_end
        context = {
            'contest_state': contest_state,
            'contest': self,
        }
        return template.render(context)
