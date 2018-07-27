from django.contrib import admin
from .models import Bukkake
from .models import Comment

# Register your models here.
class BukkakeAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created', 'updated']
    list_filter = ['created', 'updated']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['commented_by', 'created_on']

admin.site.register(Bukkake, BukkakeAdmin)
admin.site.register(Comment, CommentAdmin)
