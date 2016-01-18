from __future__ import unicode_literals
from future.builtins import str

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine.utils.models import AdminThumbMixin, upload_to
from apps.galleries.models import Gallery
from apps.portal.models import Country
#from topnotchdev import files_widget


def post_upload_to(instance = None):
    return instance.blog.slug if instance else ''

def blog_upload_to(instance = None):
    return instance.slug if instance else ''

class Blog(Displayable, Ownable):
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=blog_upload_to,
        format="Image", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("blog_list", (), {'username': self.user.username})

class BlogPost(Displayable, Ownable, RichText, AdminThumbMixin):
    """
    A blog post.
    """

    #images = files_widget.ImagesField()
    blog = models.ForeignKey(Blog, verbose_name=_("Blog"),
                             related_name="%(class)ss")
    country = models.ForeignKey(Country, verbose_name=_("Country"),
                             related_name="%(class)ss")
    gallery = models.ForeignKey(Gallery, verbose_name=_("Gallery"),
                                blank=True, null=True,
                                related_name="%(class)ss")
    map_url = models.CharField(_("Map URL"), max_length=2000, 
                               blank=True, null=True,
                               help_text=_("Google Maps URL"))
    categories = models.ManyToManyField("BlogCategory",
                                        verbose_name=_("Categories"),
                                        blank=True, related_name="blogposts")
    allow_comments = models.BooleanField(verbose_name=_("Allow comments"),
                                         default=True)
    comments = CommentsField(verbose_name=_("Comments"))
    rating = RatingField(verbose_name=_("Rating"))
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=post_upload_to,
        format="Image", max_length=255, null=True, blank=True)
    related_posts = models.ManyToManyField("self",
                                 verbose_name=_("Related posts"), blank=True)

    admin_thumb_field = "featured_image"

    class Meta:
        verbose_name = _("Blog post")
        verbose_name_plural = _("Blog posts")
        ordering = ("-publish_date",)

    def get_absolute_url(self):
        """
        URLs for blog posts can either be just their slug, or prefixed
        with a portion of the post's publish date, controlled by the
        setting ``BLOG_URLS_DATE_FORMAT``, which can contain the value
        ``year``, ``month``, or ``day``. Each of these maps to the name
        of the corresponding urlpattern, and if defined, we loop through
        each of these and build up the kwargs for the correct urlpattern.
        The order which we loop through them is important, since the
        order goes from least granular (just year) to most granular
        (year/month/day).
        """
        url_name = "blog_post_detail"
        #TODO create user slug
        kwargs = {"username": self.user.username, 
                  "blog_slug": self.blog.slug,
                  "post_slug": self.slug
                 }
        date_parts = ("year", "month", "day")
        if settings.BLOG_URLS_DATE_FORMAT in date_parts:
            url_name = "blog_post_detail_%s" % settings.BLOG_URLS_DATE_FORMAT
            for date_part in date_parts:
                date_value = str(getattr(self.publish_date, date_part))
                if len(date_value) == 1:
                    date_value = "0%s" % date_value
                kwargs[date_part] = date_value
                if date_part == settings.BLOG_URLS_DATE_FORMAT:
                    break
        return reverse(url_name, kwargs=kwargs)

    # These methods are deprecated wrappers for keyword and category
    # access. They existed to support Django 1.3 with prefetch_related
    # not existing, which was therefore manually implemented in the
    # blog list views. All this is gone now, but the access methods
    # still exist for older templates.

    def category_list(self):
        from warnings import warn
        warn("blog_post.category_list in templates is deprecated"
             "use blog_post.categories.all which are prefetched")
        return getattr(self, "_categories", self.categories.all())

    def keyword_list(self):
        from warnings import warn
        warn("blog_post.keyword_list in templates is deprecated"
             "use the keywords_for template tag, as keywords are prefetched")
        try:
            return self._keywords
        except AttributeError:
            keywords = [k.keyword for k in self.keywords.all()]
            setattr(self, "_keywords", keywords)
            return self._keywords


class BlogCategory(Slugged):
    """
    A category for grouping blog posts into a series.
    """

    blog = models.ForeignKey(Blog, verbose_name=_("Blog"),
                             related_name="%(class)ss")
    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
        ordering = ("title",)

    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_list_category", (), {"category": self.slug})
