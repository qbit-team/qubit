from django.contrib import admin
from .models import Mail

class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'sender', 'receiver', 'release', 'is_read')

admin.site.register(Mail, MailAdmin)