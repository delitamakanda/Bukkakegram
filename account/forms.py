from django import forms
from django.contrib.auth.models import User
from .models import Profile, ChatMessage
from django.core.validators import RegexValidator
import bleach
import markdown
from django.utils.html import escape
import re

# TODO: A supprimer
# class LoginForm(forms.Form):
    # username = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email',)

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']



class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo',)


class AdminChatMessageForm(forms.ModelForm):

    class Meta:
        model = ChatMessage
        fields = ['user', 'message', 'message_html']

    def clean(self):
        message = self.cleaned_data['message']

        message_html = escape(message)

        urlRegex = re.compile(
                u'(?isu)(\\b(?:https?://|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)[^\\s()<'
                u'>\\[\\]]+[^\\s`!()\\[\\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019])'
            )
        processed_urls = list()
        for obj in urlRegex.finditer(current_message):
            old_url = obj.group(0)
            if old_url in processed_urls:
                continue
            processed_urls.append(old_url)
            new_url = old_url
            if not old_url.startswith(('https://', 'http://')):
                new_url = 'http://' + new_url
            new_url = '<a href="'+ new_url + '">' + new_url + '</a>'
            message_html = message_html.replace(old_url, new_url)

        self.cleaned_data['message_html'] = message_html

        return self.cleaned_data
