from django.contrib import admin
from .models import Bukkake

# Register your models here.
class BukkakeAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created']
    list_filter = ['created']

admin.site.register(Bukkake, BukkakeAdmin)
