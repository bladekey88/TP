from django.contrib import admin
from .models import Document,ProcessDocument, Question, Subject, Topic
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.conf.locale.es import formats as es_formats

es_formats.DATETIME_FORMAT = "d M Y H:i:s"

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

class ProcessDocumentAdmin(admin.ModelAdmin):
    list_display = ['processed_id', 'document_id','processed_by','processed_at', ]  
    search_fields = ['document_id', 'processed_by']
    ordering = ['-processed_at']
    readonly_fields = ('document_id', )  
    list_display_links = list_display    
    list_select_related = ('processed_by', )
    list_filter  = ['processed_by', 'processed_at']
    list_select_related = True
    save_on_top = True
    show_full_result_count = True
    
admin.site.register(Document, DocumentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Topic)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ProcessDocument,ProcessDocumentAdmin)