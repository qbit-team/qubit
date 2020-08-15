from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,blank=True, null=True)
    text = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    pin = models.IntegerField(blank=True)
    title = models.TextField(blank=True)
    tag = models.CharField(max_length=1000, blank=True)
    release_date = models.DateTimeField(auto_now=True)
    is_comment = models.BooleanField()
    is_visible = models.BooleanField()