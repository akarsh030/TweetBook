from __future__ import unicode_literals
from django.db import models
from authentication.models import Account
import os
# Create your models here.
class posts(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    text = models.TextField()
    pmedia = models.FileField(upload_to='posts/')
    creation_date = models.DateTimeField(auto_now_add=True)
    #
    # def __unicode__(self):
    #     return self.name

class comments(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    text = models.TextField()
    post=models.ForeignKey(posts,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    #
    # def __unicode__(self):
    #     return self.list