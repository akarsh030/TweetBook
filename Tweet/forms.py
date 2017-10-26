
from django.forms import ModelForm
from .models import *

class postsForm(ModelForm):
    class Meta:
        model=posts
        fields=['text','user','pmedia']

class commsForm(ModelForm):
    class Meta:
        model=comments
        fields=['text','user','post']