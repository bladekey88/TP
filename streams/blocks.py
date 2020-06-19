'''StreamField'''

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

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
        self.features = ['bold', 'italic', 'link', 'h5', 'ul', 'li','image', 'superscript',]

    class Meta:
        label = "Section Content"      
        

class InfoBlock(blocks.RichTextBlock):
    '''Info block '''

    def __init__(self, required=False, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = ['bold', 'italic', 'h5', 'supercript','superscript',]
        self.help_text= 'This field is used to draw attention to something or highlight something of intrest'
    
    
    
    class Meta:
        label = "Highlight" 
        template = 'streams/info.html'  
        icon="info"  
    
    
        
class LessonContentBlock(blocks.StructBlock):
    '''Block containing Lesson Content. Each block will be wrapped ina section for css purposes'''
    
    title = blocks.CharBlock(required=True, label="Section Title",help_text="Add Section Title",max_length=40)
    text = LessonBlock(required=True, help_text="Add Section Content")

    class Meta:
        template = 'streams/lesson_content_block.html'
        icon = "doc-full"
        label = "Lesson Sections"
        help_text = "Each lesson section will cause  a link to be added to  sidebar for ease of navigation. Each section must have a title along with its content."


class SubjectBlock(blocks.StructBlock):
    subject_name = blocks.CharBlock(required=True,label="Subject Name",max_length=30)
    subject_image = ImageChooserBlock(required=True, label="Subject Image")
    subject_page = blocks.PageChooserBlock(required=True, page_type="subject.SubjectLandingPage")
    
    class Meta:
        template = 'streams/subject_block.html'