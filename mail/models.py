from django.db import models
from django.contrib.auth.models import User

class Mail (models.Model):
    sender = models.ForeignKey(User, related_name="mail_sender")
    receiver = models.ForeignKey(User, related_name="mail_receiver")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="mail_parent", null=True, blank=True)
    grand_parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="mail_grand_parent", null=True, blank=True)
    text = models.TextField(blank=True)
    topic = models.CharField(max_length = 1000, blank=True)
    release = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField() # by receiver
    is_reply = models.BooleanField()
