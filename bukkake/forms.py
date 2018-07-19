import ssl

from urllib.request import urlopen
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Bukkake

class BukkakeCreateForm(forms.ModelForm):

    class Meta:
        model = Bukkake
        fields = ('title', 'url', 'description', 'filters',)
        widget = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg'] # png or gif not permit due to Pillow restrictions
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(BukkakeCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())

        # download image from the url
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urlopen(image_url, context=ctx)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()
        return image
