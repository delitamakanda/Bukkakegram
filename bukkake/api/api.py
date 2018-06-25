from tastypie.resources import ModelResource
from bukkake.models import Bukkake

class BukkakeResource(ModelResource):

    class Meta:
        queryset = Bukkake.objects.all()
        resource_name = 'bukkake'
