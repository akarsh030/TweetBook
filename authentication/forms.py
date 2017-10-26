
from django.forms import ModelForm
from .models import *

class accountsForm(ModelForm):
    class Meta:
        model=Account
        fields=['username','email','firstname','lastname','faculty','is_faculty','dp','phone']