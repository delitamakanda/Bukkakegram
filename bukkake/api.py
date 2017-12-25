from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from bukkake.models import Bukkake
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from django.contrib.auth.models import User
from tastypie import fields, utils
from tastypie.throttle import BaseThrottle, CacheThrottle
from tastypie.paginator import Paginator


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        authorization = DjangoAuthorization()
        throttle = BaseThrottle(throttle_at=100)
        filtering = {
            'username': ALL,
        }


class BukkakeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        allowed_methods = ['get']
        queryset = Bukkake.objects.all()
        resource_name = 'bukkake'
        authorization = Authorization()
        authentication = BasicAuthentication()
        throttle = CacheThrottle()
        paginator_class = Paginator
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
