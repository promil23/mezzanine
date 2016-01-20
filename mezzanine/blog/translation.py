from modeltranslation.translator import translator
from mezzanine.core.translation import (TranslatedSlugged,
                                        TranslatedDisplayable,
                                        TranslatedRichText)
from apps.portal.models import BlogPost, BlogCategory


class TranslatedBlogPost(TranslatedDisplayable, TranslatedRichText):
    fields = ()


class TranslatedBlogCategory(TranslatedSlugged):
    fields = ()

translator.register(BlogCategory, TranslatedBlogCategory)
translator.register(BlogPost, TranslatedBlogPost)
