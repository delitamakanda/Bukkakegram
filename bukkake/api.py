from tastypie.resources import ModelResource
from bukkake.models import Bukkake
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']


class BukkakeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Bukkake.objects.all()
        resource_name = 'bukkake'
        authorization = Authorization()
