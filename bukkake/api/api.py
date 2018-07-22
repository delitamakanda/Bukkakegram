import datetime

from tastypie import fields
from tastypie.authorization import Authorization
from django.utils.timezone import utc
from django.contrib.auth.models import User

from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from bukkake.models import Bukkake
from account.models import Profile


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        detail_allowed_methods = ['get']
        excludes = ['password', 'is_active', 'email', 'is_staff','is_superuser']
        filtering = {
            'username': ALL,
        }


class ProfileResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Profile.objects.all()
        detail_allowed_methods = ['get']
        resource_name = 'profile'


class BukkakeResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')
    filters = fields.CharField(attribute='get_filters_display')

    class Meta:
        queryset = Bukkake.objects.all()
        detail_allowed_methods = ['get', 'post']
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'title': ['startswith', 'istartswith', 'exact', 'iexact']
        }
        resource_name = 'bukkake'
        authorization = Authorization()


    def obj_create(self, bundle, **kwargs):
        return super(BukkakeResource, self).obj_create(bundle, user=bundle.request.user)


    def get_filters(self, obj):
        return obj.get_filters_display()
