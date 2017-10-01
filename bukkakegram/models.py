from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone

# Create your models here.
class Bukkake(models.Model):
  user = models.ForeignKey(User)
  name = models.CharField(max_length=100)
  value = models.DecimalField(max_digits=10,decimal_places=2, blank=True, null=True)
  material = models.CharField(max_length=100, blank=True, null=True)
  location = models.CharField(max_length=100, blank=True, null=True)
  description = models.TextField()
  created_date = models.DateTimeField(default=timezone.now)
  image = CloudinaryField('image')
  likes = models.IntegerField(default=0)

  def get_absolute_url(self):
      return self.id

  def __str__(self):
    return self.name
