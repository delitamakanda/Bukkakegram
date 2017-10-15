import redis
from django.conf import settings

#connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import BukkakeCreateForm
from .models import Bukkake
from actions.utils import create_action
from django.db.models import Count

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
        form = BukkakeCreateForm(data=request.GET)

    return render(request, 'bukkakes/image/create.html', {'section': 'bukkakes', 'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Bukkake, id=id, slug=slug)
    # increment views by 1
    total_views = r.incr('image:{}:views'.format(image.id))
    # increment image ranking by 1
    r.zincrby('image_ranking', image.id, 1)
    return render(request, 'bukkakes/image/detail.html', {'section': 'bukkakes', 'image': image, 'total_views': total_views })


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
    #get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Bukkake.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'bukkakes/image/ranking.html', {'most_viewed': most_viewed})
