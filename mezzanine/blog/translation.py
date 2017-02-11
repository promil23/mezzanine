from modeltranslation.translator import translator
from mezzanine.core.translation import (TranslatedSlugged,
                                        TranslatedDisplayable,
                                        TranslatedRichText)
from apps.portal import models as bct_models


class TranslatedBlogPost(TranslatedDisplayable, TranslatedRichText):
    fields = ()


#class TranslatedBlogCategory(TranslatedSlugged):
#fields = ()
#    pass

class TranslatedBlog(TranslatedDisplayable, TranslatedRichText):
    fields = ()

translator.register(bct_models.BlogPost, TranslatedBlogPost)
translator.register(bct_models.Blog, TranslatedBlog)
