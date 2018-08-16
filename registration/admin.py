from django.contrib import admin
from registration.models import Profile, ChatMessage
from registration.forms import AdminChatMessageForm

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    form = AdminChatMessageForm
    list_display = ('user', 'message', 'message_html', 'updated', 'created',)




admin.site.register(Profile, ProfileAdmin)
