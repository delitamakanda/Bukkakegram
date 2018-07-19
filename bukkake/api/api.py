import datetime

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from django.utils.timezone import utc

from tastypie.resources import ModelResource
from bukkake.models import Bukkake

class BukkakeResource(ModelResource):

    class Meta:
        queryset = Bukkake.objects.all()
        detail_allowed_methods = ['get']
        filtering = {
            'title': ['startswith', 'istartswith', 'exact', 'iexact']
        }
        resource_name = 'bukkake'
