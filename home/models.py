from django.db import models

from wagtail.admin.edit_handlers import FieldPanel,PageChooserPanel,StreamFieldPanel, ObjectList,TabbedInterface, MultiFieldPanel
from wagtail.core.fields import RichTextField,StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks
class HomePage(Page):
    '''Home Page Model'''

    templates = "templates/home_page/html"
    max_count = 1

    banner_title = models.CharField(max_length=50, blank=False, null=True)

    banner_subtitle = RichTextField(
        features=['bold', 'italic'], max_length=100, blank=True, null=True)

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+"
    )

    Information = StreamField(
        [
            ("info_cards",blocks.CardBlock(blank=True, null=True)),         
        ],
        blank=False,
        null=True,
        help_text="This section holds the data for the four information cards displayed under the banner.",
    )
    
    Question_Generator = StreamField(
        [
            ("question_cards",blocks.CardQuestionBlock(blank=False, null=True)),         
        ],
        blank=False,
        null=True,
        help_text="This section holds the data for the QuestionGenerator Information Cards. A minimim of three is required, and a maximum of six can created",        
    )

    Promotional_Users = StreamField(
        [
            ("promotional_section",blocks.CardPromoBlock(blank=False, null=True)),         
        ],
        help_text="This section holds the data for User Promotional Section cards.",        
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                ImageChooserPanel('banner_image'),
            ],
            heading = "Banner Options"
        ),             
    ]

    information_panels = [
         StreamFieldPanel("Information"), 
    ]
    
    generator_panels = [
         StreamFieldPanel("Question_Generator"),          
    ]
    
    promotional_panels = [
         StreamFieldPanel("Promotional_Users"),          
    ]
    
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels,heading="General Settings"),
            ObjectList(information_panels, heading="Information Section"),
            ObjectList(generator_panels, heading="Question Generator Section"),
            ObjectList(promotional_panels, heading="Promotional Section"),
        ]
    )
    
    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
