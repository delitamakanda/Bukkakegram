from django.conf.urls import url
from django.conf import settings
from django.views.generic import TemplateView, RedirectView
from django.views.static import serve
from . import views

urlpatterns = [
    url(r'^user/(\w+)/$', views.profile, name='profile'),
    url(r'^$', views.index, name='index'),
    url(r'^([0-9]+)/$', views.detail, name='detail'),
    url(r'^post_url/$', views.post_bukkake, name="post_bukkake"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'^like_bukkake/$', views.like_bukkake, name='like_bukkake'),
    url(r'^register/$', views.register_view, name="register"),
    url(r'^about/$', TemplateView.as_view(template_name='other/about.html'), name='about'),
    url(r'^$', RedirectView.as_view(pattern_name='browse')),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT,}),
    ]
