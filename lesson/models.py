from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from home.models import  HomePage
from streams import blocks
from django.utils import timezone

from wagtail.admin.edit_handlers import(
    RichTextField, 
    FieldPanel, 
    StreamFieldPanel, 
    RichTextFieldPanel,  
    PageChooserPanel, 
    MultiFieldPanel,
    TabbedInterface,
    ObjectList,
    )
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable


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



class TrackUserPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=False)
    last_access = models.DateTimeField(auto_now=False)
    status = models.CharField(max_length = 30, default="NS",
                    choices=[
                        ("NS","NOT STARTED"),
                        ("IP", "IN PROGRESS"),
                        ("CO", "COMPLETE"),
                        ("AB", "ABANDONED"),
                    ]
                              )
    class Meta:
        unique_together=[['user','page']]
    
    def __str__(self):
        return(self.user.username)

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
        
    section_content = StreamField(
        [
            ("test", blocks.LessonContentBlock()),   
            ('info', blocks.InfoBlock()),         
        ],
        null=True,
        blank=True
    )
     
    content_panels = Page.content_panels + [
            MultiFieldPanel(  
                [                        
                    FieldPanel("lesson_name"),
                    FieldPanel("lesson_summary"),
                    FieldPanel("presentation_link"),                            
                ],
                heading = "Lesson Information",
                classname="collapsible",
            )
    ]
    
    section_content_panels =  [
        MultiFieldPanel(
            [
                StreamFieldPanel("section_content")
            ],
            heading="Section Content",
            classname="collapsible", 
            ),
        ]
    
    edit_handler = TabbedInterface(
            [
                ObjectList(content_panels, heading='General Information'),
                ObjectList(section_content_panels, heading='Lesson Content'),
                ObjectList(Page.promote_panels, heading='Promote'),
                ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
            ]    
        )
    
    def get_context(self,request,*args,**kwargs):
        context = super().get_context(request,*args,**kwargs)
        context['subject_name'] = self.get_ancestors(inclusive=True).not_type(HomePage).exclude(title__contains="Root")        
        context['key_stage'] = self.get_parent()
        context['siblings'] = self.get_siblings()
        self.tracking(request)
        return context

    def tracking(self,request):
        current_user = request.user
        track = TrackUserPage()
        current_time = timezone.now()
        user_started_lesson = TrackUserPage.objects.filter(user=current_user,page=self.id)
                
        if not user_started_lesson.exists():
            print("user id" + str(current_user.id))
            track.user = request.user
            track.page = self
            track.status = "IP"
            track.start_date = current_time
            track.last_access = current_time
            return track.save()
        else:
          return user_started_lesson.update(last_access= current_time)