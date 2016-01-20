from __future__ import unicode_literals

from functools import update_wrapper
from copy import deepcopy
from urllib.parse import urlparse, parse_qs

from django.contrib import admin
from django.views.generic import RedirectView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.utils import unquote

from apps.portal.models import Blog, BlogPost, BlogCategory
from mezzanine.conf import settings
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.twitter.admin import TweetableAdminMixin

blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
#TODO remove blog from blogpost
#blogpost_fieldsets[0][1]["fields"].insert(0, "images")
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
    def changelist_view(self, request, form_url='', 
                             extra_context=None):
        extra_context = extra_context or {}
        #TODO error handling if no blog
        blog_id = request.GET['blog']
        extra_context['blog'] = Blog.objects.get(id = blog_id)
        return super(BlogPostAdmin, self).changelist_view(request, extra_context=extra_context)

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        opts = self.model._meta
        app_label = opts.app_label
        preserved_filters = self.get_preserved_filters(request)
        form_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, form_url)

        if add:
            #print(form_url)
            form_url += '&blog=1'
        return super(BlogPostAdmin, self).render_change_form(request, context, add, change, form_url, obj)

    #TODO @csrf_protect_m and @transaction.atomic
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)
        extra_context = extra_context or {}
        add = object_id is None

        if add:
            #TODO error handling if no blog
            blog_id = request.GET['blog']
            extra_context['original'] = {'blog': Blog.objects.get(id = blog_id)}
        else:
            post_obj = self.get_object(request, unquote(object_id), to_field)
        return super(BlogPostAdmin, self).changeform_view(request, object_id, form_url, extra_context)

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
            if "portal.BlogCategory" in items:
                return True
        return False


#admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
