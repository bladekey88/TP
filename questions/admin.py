from django.contrib import admin
from .models import Subject, Topic



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

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic)