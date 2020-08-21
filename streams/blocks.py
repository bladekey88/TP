'''StreamField'''

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalManyToManyField
from wagtail.snippets.blocks import SnippetChooserBlock

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

class TitleAndTextBlock(blocks.StructBlock):
    '''Title and Text'''

    title = blocks.CharBlock(required=True, help_text="Add Your Title")
    text = blocks.CharBlock(required=True, help_text="Add Additional Text")

    class Meta:
        template = 'streams/title_and_text_block.html'
        icon = "edit"
        label = "Title and Text"


class RichTextBlock(blocks.RichTextBlock):
    '''Rich Text Block with all features'''

    class Meta:
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full Richtext Editing"


class LimitedRichTextBlock(blocks.RichTextBlock):
    '''Rich Text only with Subset'''

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = ['bold', 'italic', 'link']

    class Meta:
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Basic Richtext Editing"



class SubjectModuleBlock(blocks.StructBlock):
    '''Page Chooser Block'''
    
    module_name =  blocks.PageChooserBlock(required="True",help_text="Select Module",can_choose_root=False)
    module_information = blocks.CharBlock(required=True, help_text="Add Module Information")
    
       
    class Meta:
        template = "streams/subject_module_block.html"
        icon = "doc-full"
        label = "Add Module Information"
        
       
       
class LessonBlock(blocks.RichTextBlock):
    '''Rich Text only with Subset used for lesson '''
    '''@TODO add chemistry and mathematics  specific functions '''
    
    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = ['bold', 'italic', 'link', 'h5', 'ul', 'ol','li','image', 'superscript', 'subscript']

    class Meta:
        label = "Section Content"      
 
class InfoBlock(blocks.RichTextBlock):
    '''Info block '''

    def __init__(self, required=False, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = ['bold', 'italic', 'h5', 'supercript','superscript',]
        self.help_text = 'This field is used to draw attention to something or highlight something of intrest'

    class Meta:
        label = "Highlight" 
        template = 'streams/info.html'  
        icon="info"  
    

class LessonContentStreamBlock(blocks.StreamBlock):
    lesson_content =blocks.StructBlock( [
      ('targetted_level',blocks.CharBlock(default="All", required=True,help_text="This is only displayed when using more than one content block",label="Targetted Level")),
      ('section_content',LessonBlock(required=True))
    ])

    class Meta:
        label = "Section Content"
        icon = "doc-empty-inverse"
        help_text="Sections must contain at least one content block. For section that have different requirements depending on level (e.g. Intermediate vs Higher), multiple sections can be added. It is then recommended to fill in the Content Title to differentiate the content."

class LessonContentBlock(blocks.StructBlock):
    '''Block containing Lesson Content. Each block will be wrapped ina section for css purposes'''
    
    title = blocks.CharBlock(required=True, label="Section Title",help_text="Add Section Title",max_length=40)
    lesson_text = LessonContentStreamBlock(max_num=3, min_num=1, required=True, help_text="Add Section Content")
    
    class Meta:
        template = 'streams/lesson_content_block.html'
        icon = "doc-full"
        label = "Lesson Section"
        help_text = "Each lesson section will cause  a link to be added to  sidebar for ease of navigation. Each section must have a title along with its content."


class SubjectBlock(blocks.StructBlock):
    subject_name = blocks.CharBlock(required=True,label="Subject Name",max_length=30)
    subject_icon = blocks.CharBlock(required=True,label="FontAwesome Subject Icon",min_length=5, max_length=20, help_text="Insert icon name from FA website. For example <i class='fas fa-adjust'></i> should be entered as fa-adjust", default="fa-")
    subject_description = blocks.CharBlock(required=True, label="Subject description", max_length=70)
    subject_page = blocks.PageChooserBlock(required=False, page_type="subject.SubjectLandingPage",)
    subject_categories = SnippetChooserBlock('subject.SubjectCategory',required=True,)
    
    class Meta:
        template = 'streams/subject_block.html'    
       
class ModuleLessonDescriptionBlock(blocks.StructBlock):
    lesson_title = blocks.CharBlock(required=True, label="Lesson Name",max_length=50)
    lesson_description = blocks.CharBlock(required=True, label="Lesson Description",max_length=200)
    lesson_page = blocks.PageChooserBlock(required=False, page_type="lesson.Beta")
    
    class Meta:
        template = 'streams/module_lesson_description_block.html'
        
class ModuleLessonSummaryBlock(blocks.StructBlock):
    lesson_chapter = blocks.CharBlock(required=True, label = "Chapter Name", max_length = 100, default="e.g. Chapter xx: Introduction")
    # lesson_page = blocks.PageChooserBlock(required=True, page_type="lesson.Beta")
    lesson_info = blocks.StreamBlock(
        [
            ('lesson_page', ModuleLessonDescriptionBlock ())
        ],
        blank=False,
        null=False,
        label = "Lesson Page", 
        page_type="lesson.Beta"
    )
    class Meta:
        template = 'streams/module_lesson_summary_block.html'
        

class CardStreamBlock(blocks.StreamBlock):
    information_content =blocks.StructBlock( [
      ('Image',ImageChooserBlock( required=True,help_text="This is the header image of the card",label="Information Card Image")),
      ('Icon',blocks.CharBlock(required=True)),
      ('Title',blocks.CharBlock(required=True)),
      ('Text',blocks.CharBlock(required=True)),   
      ('BootStrap_Color', blocks.CharBlock(required=False, max_length=7, min_length=0))   
    ])

    class Meta:
        icon = "doc-empty-inverse"
        
class CardQuestionStreamBlock(blocks.StreamBlock):
    geneartor_promo_content =blocks.StructBlock( [
      ('Icon',blocks.CharBlock(required=True)),
      ('Title',blocks.CharBlock(required=True)),
      ('Text',blocks.CharBlock(required=True)),     
      ('URL',blocks.URLBlock(required=False, label="URL (Optional)")) ,
      ('link_title',blocks.CharBlock(required=False, label="URL Title")) ,
      
    ])

    class Meta:
        icon = "doc-empty-inverse"
        label = "Question Generator Promotional Card"
        
       
class CardBlock(blocks.StructBlock):
    information_title = blocks.CharBlock(required=True, max_num=1, length=40)
    information_cards = CardStreamBlock(required=True, min_num=4,max_num=4, help_text="Add Information Cards")
    
    class Meta:
        template = 'streams/card_info_block.html'
        icon = "help"
        
class CardQuestionBlock(blocks.StructBlock):
    question_title = blocks.CharBlock(required=True, max_num=1, length=40, label="Question Generator Section Heading", default="Our Question Generator lets you")
    question_cards = CardQuestionStreamBlock(required=True, min_num=3,max_num=6, help_text="Add Question Cards")

    class Meta:
        template = 'streams/card_generator_block.html'
        icon = "help"
               
class CardPromoBlock(blocks.StructBlock):           
    promo_title = blocks.CharBlock(required=True, max_num=1, length=40, label="Promo Section Heading", default="Designed for Students and Teachers")
    promo_user_cards = CardStreamBlock(required=True, min_num=4,max_num=4, help_text="Add Promotional User Cards")
    
    class Meta:
        template = 'streams/card_promo_block.html'
        icon = "help"
            

