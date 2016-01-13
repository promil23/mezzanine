from __future__ import unicode_literals

from functools import update_wrapper
from copy import deepcopy

from django.contrib import admin
from django.views.generic import RedirectView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from mezzanine.blog.models import Blog, BlogPost, BlogCategory
from mezzanine.conf import settings
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.twitter.admin import TweetableAdminMixin

blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
#TODO remove blog from blogpost
blogpost_fieldsets[0][1]["fields"].insert(1, "blog")
blogpost_fieldsets[0][1]["fields"].insert(2, "country")
blogpost_fieldsets[0][1]["fields"].insert(3, "gallery")
blogpost_fieldsets[0][1]["fields"].insert(4, "map_url")
blogpost_fieldsets[0][1]["fields"].insert(5, "categories")
blogpost_fieldsets[0][1]["fields"].extend(["content", "allow_comments"])
blogpost_list_display = ["title", "user", "status", "admin_link"]
if settings.BLOG_USE_FEATURED_IMAGE:
    blogpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
    blogpost_list_display.insert(0, "admin_thumb")
blogpost_fieldsets = list(blogpost_fieldsets)
blogpost_fieldsets.insert(1, (_("Other posts"), {
    "classes": ("collapse-closed",),
    "fields": ("related_posts",)}))
blogpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)

blog_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
if settings.BLOG_USE_FEATURED_IMAGE:
    blog_fieldsets[0][1]["fields"].append("featured_image")

class BlogAdmin(DisplayableAdmin, OwnableAdmin):
    fieldsets = blog_fieldsets
    list_display = ("title", "status", "admin_link", "blogposts_link")

    def get_urls(self):
        base_urls = super(BlogAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            #url(r'^(.+)/blogposts/change/$', wrap(self.posts_change_view), name='%s_%s_change' % info),
            #url(r'^(.+)/blogposts/$', wrap(self.posts_changelist_view), name='%s_%s_change' % info),
            url(r'^(?P<object_id>\d+)/blogposts/$', wrap(self.posts_changelist_view), name='%s_%s_change' % info),
        ]
        return urlpatterns + base_urls

    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()\
                       .filter(user = request.user)
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def posts_changelist_view(self, request, object_id, form_url='', 
                             extra_context=None):
        return HttpResponseRedirect(
               '{0}?blog_id={1}'\
               .format(reverse("admin:blog_blogpost_changelist"), object_id)
        )

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)

    def blogposts_link(self, obj):
        url = '{0}?blog={1}'\
               .format(reverse("admin:blog_blogpost_changelist"), obj.id)
        return "<a href='%s'>%s</a>" % (url, _("Posts"))

    blogposts_link.allow_tags = True
    blogposts_link.short_description = ""


class BlogPostAdmin(TweetableAdminMixin, DisplayableAdmin, OwnableAdmin):
    """
    Admin class for blog posts.
    """

    fieldsets = blogpost_fieldsets
    list_display = blogpost_list_display
    list_filter = blogpost_list_filter
    filter_horizontal = ("categories", "related_posts",)

    '''
    TODO - if new object then select first user blog
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        #print(db_field.name)
        if db_field.name == 'blog':
            kwargs['initial'] = 1#request.user.id
        return super(BlogPostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
    TODO remove unneded blogpost url
    def get_urls(self):
        base_urls = super(BlogPostAdmin, self).get_urls()
        del base_urls[0]
        return base_urls
    '''
    def get_model_perms(self, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, *args, **kwargs)
        perms['list_hide'] = True
        return perms

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


class BlogCategoryAdmin(BaseTranslationModelAdmin):
    """
    Admin class for blog categories. Hides itself from the admin menu
    unless explicitly specified.
    """

    fieldsets = ((None, {"fields": ("title",)}),)

    def in_menu(self):
        """
        Hide from the admin menu unless explicitly set in ``ADMIN_MENU_ORDER``.
        """
        for (name, items) in settings.ADMIN_MENU_ORDER:
            if "blog.BlogCategory" in items:
                return True
        return False


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
