from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView

from links.models import Link, Comment
from links.forms import CommentModelForm

# Create your views here.
class NewCreateView(CreateView):
    model = Link
    fields = (
        'title', 'url'
    )

    template_name = 'links/new.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCreateView, self).dispatch(*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewCreateView, self).get_context_data(**kwargs)
        context['section'] = 'links'
        return context

    def form_valid(self, form):
        new_link = form.save(commit=False)
        new_link.submitter = self.request.user
        new_link.save()

        self.object = new_link

        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('links-detail', kwargs={'pk': self.object.pk})


class NewDetailView(DetailView):
    model = Link

    template_name = 'links/detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewDetailView, self).get_context_data(**kwargs)

        link_comments = Comment.objects.filter(commented_on=self.object, in_reply_to__isnull=True)

        context['comments'] = link_comments
        context['comment_form'] = CommentModelForm(initial={'link_pk': self.object.pk})
        return context

class NewCommentView(CreateView):
    form_class = CommentModelForm
    http_method_names = ('post',)
    template_name = 'links/comment.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentView, self).dispatch(*args,**kwargs)

    def form_valid(self, form):
        parent_link = Link.objects.get(pk=form.cleaned_data['link_pk'])

        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_link
        new_comment.commented_by = self.request.user

        new_comment.save()

        return HttpResponseRedirect(reverse('links-detail', kwargs={'pk': parent_link.pk}))

    def get_initial(self):
        initial_data = super(NewCommentView, self).get_initial()
        initial_data['link_pk'] = self.request.GET['link_pk']

    def get_context_data(self, **kwargs):
        context = super(NewCommentView, self).get_context_data(**kwargs)
        context['submission'] = Link.objects.get(pk=self.request.GET['link_pk'])

        return context


class NewCommentReplyView(CreateView):
    form_class = CommentModelForm
    template_name = 'links/comment_reply.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentReplyView, self).dispatch(*args,**kwargs)

    def get_initial(self):
        initial_data = super(NewCommentReplyView, self).get_initial()

        link_pk = self.request.GET['link_pk']
        initial_data['link_pk'] = link_pk

        parent_comment_pk = self.request.GET['parent_comment_pk']
        initial_data['parent_comment_pk'] = parent_comment_pk

        return initial_data

    def get_context_data(self, **kwargs):
        context = super(NewCommentReplyView, self).get_context_data(**kwargs)
        context['parent_comment'] = Comment.objects.get(pk=self.request.GET['parent_comment_pk'])

        return context

    def form_valid(self, form):
        parent_link = Link.objects.get(pk=form.cleaned_data['link_pk'])
        parent_comment = Comment.objects.get(pk=form.cleaned_data['parent_comment_pk'])

        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_link
        new_comment.in_reply_to = parent_comment
        new_comment.commented_by = self.request.user

        new_comment.save()

        return HttpResponseRedirect(reverse('links-detail', kwargs={'pk': parent_link.pk}))
