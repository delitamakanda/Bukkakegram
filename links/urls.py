from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.NewCreateView.as_view(), name='new-links'),
    url(r'^(?P<pk>\d+)/$', views.NewDetailView.as_view(), name='links-detail'),
    url(r'^comment/$', views.NewCommentView.as_view(), name='new-comment'),
    url(r'^reply/$', views.NewCommentReplyView.as_view(), name='new-reply'),
    url(r'^$', views.NewListView.as_view(), name='links'),
    url(r'^upvote/(?P<link_pk>\d+)/$', views.UpVoteLinkView.as_view(), name='upvote'),
    url(r'^downvote/(?P<link_pk>\d+)/$', views.RemoveVoteLinkView.as_view(), name='downvote'),
]
