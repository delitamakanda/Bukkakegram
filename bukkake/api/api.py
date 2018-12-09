import datetime

from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from django.utils.timezone import utc
from django.contrib.auth.models import User

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from bukkake.models import Bukkake
from registration.models import Profile


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        detail_allowed_methods = ['get']
        excludes = ['password', 'is_active', 'is_staff','is_superuser']
        filtering = {
            'username': ALL,
        }

class ProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Profile.objects.all()
        detail_allowed_methods = ['get']
        resource_name = 'profile'



class BukkakeAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        obj = object_list[0]
        return obj.user == bundle.request.user


class BukkakeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    filters = fields.CharField(attribute='get_filters_display')

    class Meta:
        queryset = Bukkake.objects.all()
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'title': ['startswith', 'istartswith', 'exact', 'iexact']
        }
        resource_name = 'bukkake'
        authorization = BukkakeAuthorization()
        authentication = ApiKeyAuthentication()

     # def obj_create(self, bundle, **kwargs):
        # return super(BukkakeResource, self).obj_create(bundle, user=bundle.request.user)

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle


    def get_filters(self, obj):
        return obj.get_filters_display()
