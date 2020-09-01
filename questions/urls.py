from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.urls import include
# from django.contrib.auth.mixins import LoginRequiredMixin


app_name = 'questions'

urlpatterns = [
    path('', views.index, name='index'),
    path('subject/',views.addsubject,name="addsubject"),
]