from modeltranslation.translator import translator
from mezzanine.core.translation import (TranslatedSlugged,
                                        TranslatedDisplayable,
                                        TranslatedRichText)
from apps.portal.models import Blog, BlogPost, BlogCategory


class TranslatedBlogPost(TranslatedDisplayable, TranslatedRichText):
    fields = ()


class TranslatedBlogCategory(TranslatedSlugged):
    fields = ()

class TranslatedBlog(TranslatedDisplayable, TranslatedRichText):
    fields = ()

translator.register(BlogCategory, TranslatedBlogCategory)
translator.register(BlogPost, TranslatedBlogPost)
translator.register(Blog, TranslatedBlog)
