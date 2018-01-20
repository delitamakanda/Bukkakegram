from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Link(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    submitter = models.ForeignKey(User)
    submitted = models.DateTimeField(auto_now_add=True, editable=False)
    upvotes = models.ManyToManyField(User, related_name='votes')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('links-detail', args=[self.id])


class Comment(models.Model):
    body = models.TextField()
    commented_on = models.ForeignKey(Link)
    in_reply_to = models.ForeignKey('self', null=True)
    commented_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{}. {}'.format(self.commented_on, self.commented_by)
