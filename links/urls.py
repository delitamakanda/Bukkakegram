from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.NewCreateView.as_view(), name='links'),
    url(r'^(?P<pk>\d+)/$', views.NewDetailView.as_view(), name='links-detail'),
    url(r'^comment/$', views.NewCommentView.as_view(), name='new-comment'),
    url(r'^reply/$', views.NewCommentReplyView.as_view(), name='new-reply'),
]
