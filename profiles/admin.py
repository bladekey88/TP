from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile  
from lesson.models import TrackUserPage

class LessonTrackInline(admin.TabularInline):
    model=TrackUserPage
    can_delete=True
    verbose_name = "Lesson"
    verbose_name_plural = "Lessons"
    show_change_link = True
    min_num = 1
    max_num = 1
  

class ModelInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ModelInline,LessonTrackInline)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)