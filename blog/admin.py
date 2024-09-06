from django.contrib import admin
from .models import Blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publish_date', 'update_date', 'version')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'author', 'tags')
    list_filter = ('publish_date', 'update_date', 'author')

admin.site.register(Blog, BlogAdmin)
