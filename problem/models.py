#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from contest.models import Contest
# Create your models here.



class Problem(models.Model):
    parent_contest = models.ForeignKey('contest.Contest', on_delete=models.CASCADE, blank=True, null=True )
    code = models.CharField(max_length=200)
    #solved = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField() # text of problem
    is_visible = models.BooleanField(default = True)
    def __str__(self):
        return self.code
    def maxscore(self):
        res=0
        for subtask in self.subtask_set.all():
            res+=subtask.score
        return res
    def userscore(self,vuser):
        res=0
        for s in self.subtask_set.all():
            if s.is_accepted(vuser):
                res+=s.score
        return res
    def usertry(self,vuser):
        for s in self.subtask_set.all():
            if Submission.objects.filter(user=vuser,task=s):
                return 1
        return 0
class Subtask(models.Model):
    style_case = ( ( 'text' , 'text' ) , ( 'coq' , 'coq' ) , ('pic','pic') )
    style = models.CharField(max_length=5, choices=style_case , default = 'text')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    answer = models.TextField() #models.CharField(max_length=300) # real answer
    score = models.IntegerField()
    tag = models.CharField(max_length=200, blank=True)
    abjad_order = (
    ('A', 'الف'),
    ('B', 'ب'),
    ('C', 'ج'),
    ('D', 'د'),
    ('E', 'ه'),
    ('F', 'و'),
)
    code = models.CharField(max_length=1, choices=abjad_order)
    solution = models.TextField(blank=True) # real solution
    def __str__(self):
        return "%s_%s" % (self.problem.code, self.code)
    def is_accepted(self,vuser):
        if Submission.objects.filter(user=vuser,task=self,verdict=1):
            return 1
        else:
            return 0

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Subtask, on_delete=models.CASCADE)
    release_date = models.DateTimeField(auto_now_add=True)
    verdict = models.IntegerField()
    context = models.TextField(blank=True)
    judge_log = models.TextField(blank=True)
    def __str__(self):
        return "%s_%s" % (self.user, self.task)
