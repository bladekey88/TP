from django.db import models
from django import forms
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, RichTextFieldPanel, InlinePanel, PageChooserPanel, MultiFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalManyToManyField

from streams import blocks
from lesson.models import Beta

class SubjectPage(Page):
    '''Page with all subjects on'''
    
    templates = 'subject/subject_page.html'
    parent_page_types = ['home.HomePage']
    max_count = 1
    
    subject =  StreamField(
        [
            ("subject", blocks.SubjectBlock()),            
        ],
        null=True,
        blank=False
     )
    
    categories = ParentalManyToManyField("subject.SubjectCategory", blank=True)
    
    content_panels = Page.content_panels + [
        StreamFieldPanel('subject'),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading = "Categories"
        )
    ]
	
class SubjectCategory(models.Model):
    '''category for snippers'''
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name = "slug",        
        allow_unicode = False,
        max_length = 255,
        help_text = "A slug to identify subejcts by category", 
        )
    
    class Meta:
        verbose_name = "Subject Category"
        verbose_name_plural = "Subject Categories"
        ordering = ["name"]
    
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]
           
    def __str__(self):
        return self.name
    
register_snippet(SubjectCategory)    
    
class SubjectLandingPage(Page):
    '''Subject Landing Page (Brief Overview of Subjects with more details'''

    templates = 'subject/subject_landing_page.html'
    parent_page_types = ["SubjectPage"]
    
    subject = models.CharField(blank=False, null=False, max_length=20, unique=True, help_text='Enter the Subject Name')
    subject_quote = RichTextField(blank=True, null=True, max_length=300,features=['h5', 'bold', 'italic', ])    
    subject_content = RichTextField(blank=False, null=True, features=['h5', 'bold', 'italic', 'link','ol','ul','superscript','subscript'])
    subject_image =  models.ForeignKey('wagtailimages.Image',null=True,blank = False,on_delete = models.SET_NULL,related_name = "+",help_text = "This will be used on the landing page and will be cropped")
        
    content_panels = Page.content_panels + [
        FieldPanel('subject', heading='Subject Name'),
        RichTextFieldPanel('subject_quote', heading='Subject Quote (Flavour Text)'),
        RichTextFieldPanel('subject_content', heading='Subject Information'),
        ImageChooserPanel('subject_image', heading="Subject Image"),
    ]

    class Meta:
        verbose_name = 'Subject Overview Page'
        verbose_name_plural = 'Subject Overview Pages'
        
    def __str__(self):
        return self.title


    def get_context(self,request,*args,**kwargs):
        context = super().get_context(request,*args,**kwargs)
        # context["keystages"] = SubjectKSLandingPage.objects.live().public()
        context['keystages'] = SubjectKSLandingPage.objects.live().public().filter(title__icontains=self.subject)
        context['SubjectLandingPage'] = self        
        return context

class SubjectKSLandingPage(Page):
        '''KS Landing Page Per Subject'''
                
        class Meta:
            verbose_name = "Key Stage Description for Subject"
        
        templates  = 'subject/subject_ks_landing_page.html'
        parent_page_types = ["subject.SubjectLandingPage"]
               
        description = models.TextField(
            blank=False, 
            null=True,
            max_length= 200,
            help_text = "Please enter a short description as to what this Key Stage covers"
        )    
        
        image = models.ForeignKey(
            'wagtailimages.Image',
            null=True,
            blank = False,
            on_delete = models.SET_NULL,
            related_name = "+",
            help_text = "This will be used on the listing page and will be cropped"
        )
          
        content_panels = Page.content_panels + [
        
            FieldPanel('title', heading="Key Stage"),
            RichTextFieldPanel('description'),
            ImageChooserPanel('image'),            
         ]
        
        def get_context(self,request,*args,**kwargs):
            context = super().get_context(request,*args,**kwargs)
            context["modules"] = self.get_children().live().public()
            return context


class ModuleLandingPage(Page):
        '''Landing Page for each module with a list of all the lessons on'''
        class Meta:
            verbose_name = "Module Page"
        
        templates  = 'subject/module_landing_page.html'
        parent_page_types = ["subject.SubjectKSLandingPage"]

        description = RichTextField(
            blank=False, 
            null=True,
            max_length= 400,
            help_text = "Please insert a short description explaining what this module covers"
        )
        
        objectives = RichTextField(
            blank=False,
            null=True,
            max_length=400,
            help_text = "Please add the learning objectives for this module"
        )
        
        lesson_summary = StreamField(
            [
                ('module_lesson_summary', blocks.ModuleLessonSummaryBlock())
            ],
            null=True,
            blank=True,
        )
        
        content_panels = Page.content_panels + [
             RichTextFieldPanel('description'),
             RichTextFieldPanel('objectives'),  
             StreamFieldPanel('lesson_summary'),
        ] 
        
        def get_context(self,request,*args,**kwargs):
            context = super().get_context(request,*args,**kwargs)
            context["modules"] = self.get_children().live().public().specific()
            context['test'] = Beta.objects.live().public().all().specific()
            return context


# class SubjectKeyStageCard(Orderable):
#     '''Between 1 and 4 '''

#     page = ParentalKey('subject.SubjectLandingPage', related_name='key_stage_card')
#     title = models.CharField(max_length=20, null=False, blank=False, unique=True, help_text="Enter the Key Stage Level")
#     description = RichTextField(max_length=200, null=False, blank=False, help_text="Enter information about what this Key Stage covers", features=['h4', 'h5', 'bold', 'italic', ])

    
#     content = StreamField(
#         [
#             ("test", blocks.SubjectModuleBlock()),
            
#         ],
#         null=True,
#         blank=True
#     )
    
    
#     panels = [
#         FieldPanel('title', heading="Key Stage"),
#         RichTextFieldPanel('description'),
#         StreamFieldPanel('content'),
#     ]

    