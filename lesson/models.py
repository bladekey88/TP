from django.db import models

from wagtail.admin.edit_handlers import RichTextField, FieldPanel, StreamFieldPanel, RichTextFieldPanel, InlinePanel, PageChooserPanel
from wagtail.core.models import Page, Orderable
from home.models import  HomePage
from wagtail.core.fields import StreamField, RichTextField


from streams import blocks

# Create your models here.

class LessonPage(Page):
    
    templates = 'lesson/beta.html'
    parent_page_types = ["subject.ModuleLandingPage"]
    
    lesson_name = models.CharField(
        max_length = 150,
        null=True,
        blank= True
    )
       
    presentation_link = models.URLField(max_length=200,blank=True,null=True)
    
    content_panels  = Page.content_panels + [
        FieldPanel("lesson_name"),
        FieldPanel("presentation_link")        
    ]
           
class Beta(Page):

    parent_page_types = ["subject.ModuleLandingPage"]
    templates = 'lesson/beta.html'
    lesson_name = models.CharField(
        max_length = 150,
        null=False,
        blank= False
    )     
    
    lesson_summary = RichTextField(max_length=500, null=False, blank=False, help_text="Enter a description of this lesson. Use bullet points rather than paragraphs to separate out the key ojectives. You can use up to 500 characters.", features=[ 'ul', 'bold', 'italic', ])
    presentation_link = models.URLField(max_length=200,blank=True,null=True)
        
    content = StreamField(
        [
            ("test", blocks.LessonContentBlock()),   
            ('info', blocks.InfoBlock()),         
        ],
        null=True,
        blank=True
    )
     
    content_panels = Page.content_panels + [
          
        FieldPanel("lesson_name"),
        FieldPanel("lesson_summary"),
        FieldPanel("presentation_link"),
        StreamFieldPanel("content"),
            ]
    
    def get_context(self,request,*args,**kwargs):
        context = super().get_context(request,*args,**kwargs)
        context['subject_name'] = self.get_ancestors(inclusive=True).not_type(HomePage).exclude(title__contains="Root")        
        context['key_stage'] = self.get_parent()
        context['siblings'] = self.get_siblings()
        
        return context
    
    
