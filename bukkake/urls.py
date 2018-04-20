from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.image_create, name='create'),
    url(r'^detail/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.image_detail, name='detail'),
    url(r'^like/$', views.image_like, name='like'),
    url(r'^$', views.image_list, name='list'),
    url(r'^ranking/$', views.image_ranking, name='ranking'),
    url(r'^popular/$', views.popular_images, name='popular'),
    url(r'^update/(?P<id>\d+)/$', views.update_bukkake, name='update'),
    url(r'^delete/(?P<id>\d+)/$', views.delete_bukkake, name='delete'),
]
