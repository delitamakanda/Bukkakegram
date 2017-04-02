from django.conf.urls import url, include
from django.conf import settings
#from django.views.generic import TemplateView
from django.views.static import serve
from bukkakegram.views import BukkakeSearchListView
from . import views
from django.contrib.sitemaps.views import sitemap
from bukkakegram.sitemap import (
    BukkakeSitemap,
)

sitemaps = {
    'bukkakes': BukkakeSitemap,
}

urlpatterns = [
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'^$', views.index, name='index'),
    url(r'^([0-9]+)/$', views.detail, name='detail'),
    url(r'^post_url/$', views.post_bukkake, name="post_bukkake"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^like_bukkake/$', views.like_bukkake, name='like_bukkake'),
    url(r'^register/$', views.register_view, name="register"),
    #url(r'^about/$', TemplateView.as_view(template_name='other/about.html'), name='about'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/password/$', views.password, name='password'),
    url(r'^search/$', BukkakeSearchListView.as_view(), name='blog_search_list_view'),
    url('', include('social_django.urls', namespace='social')),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT,}),
    ]
