from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.
class Bukkake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bukkakes_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    description= models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bukkakes_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Bukkake, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('bukkakes:detail', args=[self.id, self.slug])
