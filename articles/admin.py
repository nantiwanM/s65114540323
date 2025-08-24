from django.contrib import admin
from .models import Article
from tinymce.widgets import TinyMCE
from django.db import models

class ArticlePostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(Article, ArticlePostAdmin)