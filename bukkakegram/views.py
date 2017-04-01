import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Bukkake, User
from .forms import BukkakeForm, LoginForm, RegisterForm, PhotoDirectForm, PhotoUnsignedDirectForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from cloudinary.forms import cl_init_js_callbacks
from cloudinary import api # Only required for creating upload presets on the fly

#def filter_nones(d):
    #return dict((k,v) for k,v in d.iteritems() if v is not None)

# Create your views here.
def index(request):
    #defaults = dict(format="jpg", height=200, width=200)
    #defaults["class"] = "thumbnail inline"

    #samples = [
        #dict(crop="fill", radius=0),
        #dict(crop="scale"),
        #dict(crop="fit", format="png"),
        #dict(crop="thumb", gravity="face"),
        #dict(format="png", angle=0, height=None, transformation=[
            #dict(crop="fill", gravity="north", width=200, height=200, effect="sepia"),
        #]),
    #]
    #samples = [filter_nones(dict(defaults, **sample)) for sample in samples]
    bukkakes = Bukkake.objects.all().order_by('-id')
    form = BukkakeForm()
    return render(request,'bukkake/index.html', {'bukkakes': bukkakes, 'form': form})
    #return render(request, 'bukkake/index.html', #dict(bukkakes=Bukkake.objects.all(), samples=samples))

#def post_bukkake(request):
    #unsigned = request.GET.get("unsigned") == "true"

    #if (unsigned):
        # For the sake of simplicity of the sample site, we generate the preset on the fly. It only needs to be created once, in advance.
        #try:
            #api.upload_preset(PhotoUnsignedDirectForm.upload_preset_name)
        #except api.NotFound:
            #api.create_upload_preset(name=PhotoUnsignedDirectForm.upload_preset_name, unsigned=True, folder="preset_folder")

    #direct_form = PhotoUnsignedDirectForm() if unsigned else PhotoDirectForm()
    #context = dict(
        # Form demonstrating backend upload
        #backend_form = BukkakeForm(),
        # Form demonstrating direct upload
        #direct_form = direct_form,
        # Should the upload form be unsigned
        #unsigned = unsigned,
    #)
    # When using direct upload - the following call in necessary to update the
    # form's callback url
    #cl_init_js_callbacks(context['direct_form'], request)

    #if request.method == 'POST':
        # Only backend upload should be posting here
        #form = BukkakeForm(request.POST, request.FILES)
        #context['posted'] = form.instance
        #if form.is_valid():
            # Uploads image and creates a model instance for it
            #form.save()

    #return render(request, 'bukkake/upload.html', context)

#@csrf_exempt
#def direct_upload_complete(request):
    #form = PhotoDirectForm(request.POST)
    #if form.is_valid():
        #form.save()
        #ret = dict(bukkake_id = form.instance.id)
    #else:
        #ret = dict(errors = form.errors)

    #return HttpResponse(json.dumps(ret), content_type='application/json')

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
                    print("User is valid, active and authenticated")
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The password is valid, but the account has been disabled!")
                    #return render(request, 'register.html', {'form': form})
            else:
                print("The username and password were incorrect.")
                #return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
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

#def custom_404(request):
    #return render(request, '404.html', {}, status=404)
