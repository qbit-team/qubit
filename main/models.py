from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from qubit.settings import BASE_DIR
from django.utils import timezone

def user_photo_upload_function(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    import os
    try:
        os.remove(BASE_DIR + "/media/{0}/profile/photo/photo.{1}".format(instance.user.username,filename.split(".")[len(filename.split("."))-1]))
    except:
        pass
    return '{0}/profile/photo/photo.{1}'.format(instance.user.username, filename.split(".")[len(filename.split("."))-1]) # filename

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=30, blank=True)
    origin = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to=user_photo_upload_function)
    score = models.IntegerField(default = 0)
    email_verified = models.BooleanField(default=False)
    email_for_contest = models.BooleanField(default=True)
    email_for_news = models.BooleanField(default=True)
    last_active = models.DateTimeField(default=timezone.now)

class email_token (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    token = models.TextField()
    release = models.DateTimeField(auto_now_add=True)
    email = models.TextField(null=True)
class password_token (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    token = models.TextField()
    release = models.DateTimeField(auto_now_add=True)
    client_ip = models.CharField(max_length=50, blank=True)
    client_info = models.TextField()
    release_changer = models.DateTimeField(blank=True,null=True)
    client_ip_changer = models.CharField(max_length=50, blank=True, null=True)
    client_info_changer = models.TextField(blank=True,null=True)
    expiration = models.DateTimeField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

