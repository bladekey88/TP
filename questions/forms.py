from django import forms
from .models import Document, ProcessDocument, Question, Subject, Topic
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
        
class EditTopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ['topicname']
        
class DocumentForm(forms.ModelForm):
   
    class Meta:
        model = Document
        fields = ('document', 'description' , 'subject', 'document_id')        
        
        
class QuestionForm(forms.ModelForm):
     
    
    CHOICES = [('1','1 Question From Each Selected Topic'),('2', 'Questions from Any Selected Topic')]    
    number_of_questions = forms.IntegerField(min_value=1, max_value=50, required=True, label = "How many questions should be generated from all selected topics (max 50): ")

    class Meta:    
        model = Question  
        fields = ('subjectid', 'topicid', 'number_of_questions')
        
        widgets = {
            
            'topicid': forms.CheckboxSelectMultiple(attrs={'id':'topics'}),
        }

    field_order = ['subjectid', 'topicid' ,'number_of_questions' ]
    #Override params by cleaning it up :)
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.fields['topicid'].queryset = Question.objects.none()
        self.fields['topicid'].empty_label=None                
        
        
class ProcessDocumentForm(forms.ModelForm):

  class Meta:
        model = ProcessDocument
        fields = ('processed_id',)

        