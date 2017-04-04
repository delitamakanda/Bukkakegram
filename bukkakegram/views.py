import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Bukkake, User
from .forms import BukkakeForm, LoginForm, RegisterForm, PhotoDirectForm, PhotoUnsignedDirectForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from cloudinary.forms import cl_init_js_callbacks
from django.contrib import messages
from cloudinary import api # Only required for creating upload presets on the fly
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.views.generic import ListView
from social_django.models import UserSocialAuth
import operator
from django.db.models import Q

def blog_search_list_view(request):
    return render(request, 'search.html')
    #template_name = 'other/search.html'
    #model = Bukkake
    #paginate_by = 10

    #def get_queryset(self):
        #result = super(BukkakeSearchListView, self).get_queryset()


        #query = self.request.GET.get('q')
        #if query:
            #query_list = query.split()
            #result = result.filter(
                #reduce(operator.and_,
                    #(Q(name__icontains=q) for q in query_list)) |
                #reduce(operator.and_,
                    #(Q(material__icontains=q) for q in query_list))
            #)

        #return result


# Create your views here.
def index(request):
    bukkakes_list = Bukkake.objects.all().order_by('-id')
    page = request.GET.get('page', 1)
    
    paginator = Paginator(bukkakes_list, 10)
    try:
        bukkakes = paginator.page(page)
    except PageNotAnInteger:
        bukkakes = paginator.page(1)
    except EmptyPage:
        bukkakes = paginator.page(paginator.num_pages)
           
    form = BukkakeForm()
    return render(request,'bukkake/index.html', {'bukkakes': bukkakes, 'form': form})


def detail(request, bukkake_id):
    bukkake = Bukkake.objects.get(id=bukkake_id)
    return render(request, 'bukkake/detail.html', {'bukkake': bukkake})

def profile(request, username):
    user = User.objects.get(username=username)
    bukkakes = Bukkake.objects.filter(user=user)
    return render(request, 'registration/profile.html', {'username': username, 'bukkakes': bukkakes})

def post_bukkake(request):
    form = BukkakeForm(request.POST, request.FILES)
    if form.is_valid():
        #bukkake = Bukkake(name = form.cleaned_data['name'],
                            #value = form.cleaned_data['value'],
                            #material = form.cleaned_data['material'],
                            #location = form.cleaned_data['location'],
                            #img_url = form.cleaned_data['img_url'])
        bukkake = form.save(commit = False)
        bukkake.user=request.user
        bukkake.save()
    messages.success(request, 'Your bukkake is live!')
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    messages.info(request,'User is valid, active and authenticated')
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    messages.info(request,'The password is valid, but the account has been disabled!')
                    #return render(request, 'register.html', {'form': form})
            else:
                messages.error(request,'The username and password were incorrect.')
                #return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Welcome ! Please log in with id and password.')
            return HttpResponseRedirect('/login')
    #args = {}
    #args.update(csrf(request))
    #args['form'] = RegisterForm()
    #print args
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'See you soon !')
    return HttpResponseRedirect('/')

def like_bukkake(request):
    bukkake_id = request.GET.get('bukkake_id', None)

    likes = 0
    if(bukkake_id):
        bukkake = Bukkake.objects.get(id=int(bukkake_id))
        if bukkake is not None:
            likes = bukkake.likes + 1
            bukkake.likes = likes
            bukkake.save()
    return HttpResponseRedirect(likes)

def save_profile(backend, *args, **kwargs):
    if backend.name == 'google-oauth2':
        pass

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'registration/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })




@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully update.')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form})

#def verify_email(backend, user, *args, **kwarkgs):
    #if backend.name == 'google-oauth2':
        #existing_person = Bukkake.objects.get(user=kwargs.filter('detail').get('email'))
        #if not existing_person:
            #return HttpResponse("dont have an access")


#class Bukkake:
    #def __init__(self, name, value, material, location):
        #self.name = name
        #self.value = value
        #self.material = material
        #self.location = location

#bukkakes = [
    #Bukkake('Pute de Luxe', 120.00, 'Cashmere', "Budapest")
    #Bukkake('Le Bonheur', 0.00, 'Velvet', "Paris")
    #Bukkake('Musique rock', 0.99, 'Fire', "USA")
#]
