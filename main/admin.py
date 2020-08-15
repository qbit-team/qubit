from django.contrib import admin
from .models import *
from django.contrib.sessions.models import Session



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'origin', 'photo','last_active','email_verified')
admin.site.register(Profile, ProfileAdmin)

class EmailTokenAdmin(admin.ModelAdmin):
    list_display = ('user','release','used')
admin.site.register(email_token, EmailTokenAdmin)

class PasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('user','release','client_ip','expiration','used')
admin.site.register(password_token, PasswordTokenAdmin)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)
