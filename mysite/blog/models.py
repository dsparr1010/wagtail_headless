"""Blog listing and blog detail pages"""

from django.db import models
from django.shortcuts import render

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.edit_handlers import ImageChooserPanel

from streams import blocks

#THIS IS A CHANGE
class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the blog detail pages"""

    template = 'blog/blog_listing_page.html'
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Overwrites the default title')
    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public()
        context['special_link'] = self.reverse_subpage('latest_posts')
        return context

    @route(r'^latest/$', name='latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context['posts'] = context['posts'][:1]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                'location': self.full_url + self.reverse_subpage('latest_posts'),
                'lastmod': (self.last_published_at or self.latest_revision_created_at),
                'priority' : 0.9
            }
        )
        return sitemap


class BlogDetailPage(Page):
    """Blog detail page"""
    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Overwrites the default title')
    blog_image = models.ForeignKey('wagtailimages.Image', blank=False, null=True, related_name='+', on_delete=models.SET_NULL)

    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_richtext', blocks.RichtextBlock()),
            ('simple_richtext', blocks.SimpleRichtextBlock()),
            ('cards', blocks.CardBlock()),
            ('cta', blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        StreamFieldPanel('content'),
    ]


