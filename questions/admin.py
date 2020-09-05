from django.contrib import admin
from .models import Subject, Topic,Question


#Set all blank values
admin.site.empty_value_display = '(None)'

class SubjectAdmin(admin.ModelAdmin):
    fieldsets = [        
        ("Subject Information", {'fields': ['subjectname'],}),
    ]
    list_display = ('subjectname',)
    search_fields = ['subjectname']
    list_filter  = ['subjectname']
    readonly_fields = ('subjectid', )  
    ordering = ['subjectname']

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [        
        ("Question Information", {'fields': ['questiontext','questionanswer']}),
        ("Subject Information", {'fields': ['topicid', 'subjectid']}),
    ]
    list_display = ('questionid','questiontext', 'questionanswer', 'subjectid', 'topicid', )
    search_fields = ['questiontext', 'questionanswer', 'topicid__topicname', 'subjectid__subjectname']
    list_filter  = ['subjectid', 'topicid']
    readonly_fields = ('questionid', )  
    ordering = ['questionid']


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)
