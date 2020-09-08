from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import include
# from django.contrib.auth.mixins import LoginRequiredMixin


app_name = 'questions'

urlpatterns = [
    path('', views.index, name='subject'),
    path('subject/',views.addsubject,name="addsubject"),
    path('subject/<str:subjectname>', views.editSubject, name='editsubject'),
    path('subject/<str:subjectname>/delete', views.deleteSubject, name='deletesubject'),
    
    path('topic/',views.topic,name="topic"),
    path('topic/add/',views.addtopic,name="addtopic"),
    path('topic/<int:topicid>/', views.topicdetail, name='topic-detail'),
    path('topic/add/',views.addtopic, name='addtopic'),
    path('topic/<int:topicid>/edit/', views.editTopic, name='edittopic'),
    path('topic/<int:topicid>/delete/', views.deleteTopic, name='deletetopic'),
    
    path('questions/', views.question, name='question'), 
    path('question/<str:subjectname>',views.questionlist,name='questionlist'),
    
        
    path('file-upload/', views.fileupload, name='fileupload'),
    path('file-upload/success/', views.fileupload_success, name='fileuploadsuccess'),
    
    path('generate/', views.makeQuestion, name='subject_add'),
    path('ajax/load-topics/', views.load_topics, name='ajax_load_topics'),
    path('createquestions/', views.createQuestions, name='createquestions'),
]