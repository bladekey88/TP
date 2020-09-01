from django import forms
from .models import Subject
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddSubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = ['subjectname']