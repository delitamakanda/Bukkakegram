import datetime

from tastypie import fields
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
    
    def build_schema(self):
        base_schema = super(BukkakeResource, self).build_schema()
        for f in self._meta.object_class._meta.fields:
            if f.name in base_schema['fields'] and f.choices:
                base_schema['fields'][f.name].update({
                    'choices': f.choices,
                })
        return base_schema
