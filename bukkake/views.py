from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import BukkakeCreateForm
from .models import Bukkake

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
            messages.success(request, 'Bukkake added successfully.')

            return redirect(new_item.get_absolute_url())
    else:
        form = BukkakeCreateForm(data=request.GET)

    return render(request, 'bukkakes/image/create.html', {'section': 'bukkakes', 'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(Bukkake, id=id, slug=slug)
    return render(request, 'bukkakes/image/detail.html', {'section': 'bukkakes', 'image': image })


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
