from django.contrib import admin

# Register your models here.
from .models import Contest, Notification

class ContestAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'date_start', 'date_end')

admin.site.register(Contest, ContestAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'context', 'author' , 'release')

admin.site.register(Notification, NotificationAdmin)