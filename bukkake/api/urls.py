from django.conf.urls import url, include
from tastypie.api import Api
from .api import BukkakeResource

v1_api = Api(api_name='v1')
v1_api.register(BukkakeResource())

urlpatterns = [
    url(r'^', include(v1_api.urls)),
]
