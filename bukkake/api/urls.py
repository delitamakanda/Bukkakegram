from django.conf.urls import url, include
from .api import BukkakeResource

bukkake_resource = BukkakeResource()

urlpatterns = [
    url(r'^v1/', include(bukkake_resource.urls)),
]
