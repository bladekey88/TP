from django import forms
from .models import Subject, Topic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddSubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = ['subjectname']
        
class AddTopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ['topicname']        
        
        
class EditSubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = ['subjectname']    