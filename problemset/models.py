from django.db import models
from django.contrib.auth.models import User
from problem.models import Subtask, Submission

class Queue (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Subtask, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    when_release = models.DateTimeField(auto_now_add=True)
    when_judged = models.DateTimeField(null=True, blank=True)
    is_judged = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False) # Is locked for judgement?
    def __str__(self):
        return "%s_%s" % (self.user, self.task)