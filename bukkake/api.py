from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from bukkake.models import Bukkake
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User
from tastypie import fields


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        filtering = {
            'username': ALL,
        }


class BukkakeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Bukkake.objects.all()
        resource_name = 'bukkake'
        authorization = Authorization()
        authentication = BasicAuthentication()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
