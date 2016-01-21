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

from apps.portal.models import Blog, BlogPost, BlogCategory
from mezzanine.conf import settings
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.twitter.admin import TweetableAdminMixin


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
#admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
