from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
