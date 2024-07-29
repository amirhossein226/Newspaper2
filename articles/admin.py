from django.contrib import admin
from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class AdminArticle(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


# Register your models here.
admin.site.register(Article, AdminArticle)
admin.site.register(Comment)
