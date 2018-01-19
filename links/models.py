from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Link(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    submitter = models.ForeignKey(User)
    submitted = models.DateTimeField(auto_now_add=True, editable=False)
    upvotes = models.ManyToManyField(User, related_name='votes')

    def __str__(self):
        return self.title
