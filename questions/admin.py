from django.contrib import admin
from .models import Document, Question, Subject, Topic


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

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['get_file_name' , 'subject', 'uploaded_by', 'uploaded_at']
    readonly_fields = ['uploaded_by', 'uploaded_at','subject', 'get_file_path', 'get_file_name', 'document_id']
    exclude = ('document',)



class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    can_delete = False
    verbose_name_ = "Uploaded File"
    fk_name = 'uploaded_by'
    readonly_fields = ['uploaded_by', 'uploaded_at','subject', 'get_file_name', 'get_file_path', 'description']
    exclude = ('document',)


    def has_add_permission(self,request, obj=None):
        return False


admin.site.register(Document, DocumentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)
