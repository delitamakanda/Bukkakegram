import redis
from django.conf import settings

#connect to redis
if settings.DEBUG:
    r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
else:
    r = redis.from_url(settings.REDISTOGO_URL)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.http.response import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import CreateView
from .forms import BukkakeCreateForm
from .forms import CommentModelForm
from .models import Bukkake
from .models import Comment
from actions.utils import create_action
from django.db.models import Count
from django.utils import timezone

# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = BukkakeCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'bookmark image', new_item)
            messages.success(request, 'Bukkake added successfully.')

            return redirect(new_item.get_absolute_url())
    else:
        form = BukkakeCreateForm()

    return render(request, 'bukkakes/image/create.html', {'section': 'bukkakes', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Bukkake, id=id, slug=slug)
    bukkake_comments = Comment.objects.filter(commented_on=image, in_reply_to__isnull=True)
    comment_form = CommentModelForm(initial={'bukkake_pk': image.id})
    # increment views by 1
    total_views = r.incr('image:{}:views'.format(image.id))
    # increment image ranking by 1
    r.zincrby('image_ranking', image.id, 1)
    return render(request, 'bukkakes/image/detail.html', {'section': 'bukkakes', 'image': image, 'total_views': total_views, 'comment_form': comment_form, 'comments': bukkake_comments })



@login_required
def delete_bukkake(request, id):
    bukkake = Bukkake.objects.get(id=id)
    if request.user != bukkake.user:
        messages.info(request, 'You are not authorized to edit this.')
        return redirect('/')
    elif bukkake:
        bukkake.delete()
        messages.success(request, 'Bukkake deleted successfully.')
        return redirect('/')
    else:
        messages.error(request, 'An error occured')
    return render(request, 'bukkakes/image/detail.html', {'bukkake': bukkake })

@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Bukkake.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    images = Bukkake.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'bukkakes/image/list_ajax.html', {'section': 'bukkakes', 'images': images })
    return render(request, 'bukkakes/image/list.html', {'section': 'bukkakes', 'images': images })

@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Bukkake.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

    # get most popular images
    images_by_popularity = Bukkake.objects.order_by('-total_likes')[:10]
    return render(request, 'bukkakes/image/ranking.html', {'most_viewed': most_viewed, 'images_by_popularity': images_by_popularity})


class NewCommentView(CreateView):
    form_class = CommentModelForm
    http_method_names = ('post',)
    template_name = 'comment/comment.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentView, self).dispatch(*args,**kwargs)

    def form_valid(self, form):
        parent_link = Bukkake.objects.get(id=form.cleaned_data['bukkake_pk'])

        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_link
        new_comment.commented_by = self.request.user

        new_comment.save()

        return HttpResponseRedirect(reverse('bukkakes:detail', kwargs={'id': parent_link.id,'slug': parent_link.slug}))

    def get_initial(self):
        initial_data = super(NewCommentView, self).get_initial()
        initial_data['bukkake_pk'] = self.request.GET['bukkake_pk']

    def get_context_data(self, **kwargs):
        context = super(NewCommentView, self).get_context_data(**kwargs)
        context['submission'] = Bukkake.objects.get(slug=self.request.GET['bukkake_pk'])

        return context


class NewCommentReplyView(CreateView):
    form_class = CommentModelForm
    template_name = 'comment/comment_reply.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentReplyView, self).dispatch(*args,**kwargs)

    def get_initial(self):
        initial_data = super(NewCommentReplyView, self).get_initial()

        bukkake_pk = self.request.GET['bukkake_pk']
        initial_data['bukkake_pk'] = bukkake_pk

        parent_comment_pk = self.request.GET['parent_comment_pk']
        initial_data['parent_comment_pk'] = parent_comment_pk

        return initial_data

    def get_context_data(self, **kwargs):
        context = super(NewCommentReplyView, self).get_context_data(**kwargs)
        context['parent_comment'] = Comment.objects.get(pk=self.request.GET['parent_comment_pk'])

        return context

    def form_valid(self, form):
        parent_link = Bukkake.objects.get(id=form.cleaned_data['bukkake_pk'])
        parent_comment = Comment.objects.get(id=form.cleaned_data['parent_comment_pk'])

        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_link
        new_comment.in_reply_to = parent_comment
        new_comment.commented_by = self.request.user

        new_comment.save()

        return HttpResponseRedirect(reverse('bukkakes:detail', kwargs={'id': parent_link.id,'slug': parent_link.slug}))
