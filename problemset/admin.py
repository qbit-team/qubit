from django.contrib import admin

from .models import Queue

class QueueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'submission', 'when_release', 'is_judged')

admin.site.register(Queue, QueueAdmin)