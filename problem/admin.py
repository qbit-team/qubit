from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Problem)
admin.site.register(Subtask)
admin.site.register(Submission)
