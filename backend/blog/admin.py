from django.contrib import admin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Post, Section


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Section)
class SectionAdmin(TreeAdmin):
    form = movenodeform_factory(Section)
    prepopulated_fields = {'slug': ('title',)}
