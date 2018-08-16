from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
# TODO: A supprimer
# from django.contrib.auth import authenticate, login
from registration.forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from registration.models import Profile, Contact, ChatMessage
from django.contrib.auth.models import User
from actions.utils import create_action
from actions.models import Action
from django.views.generic import View

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form })

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', { 'new_user': new_user })
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', { 'user_form': user_form })

@login_required
def dashboard(request):
    # display all action by defaut exclude current user
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    actions = actions[:10]

    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({ 'status': 'ko'})
    return JsonResponse({'status': 'ko'})

# TODO: A supprimer
# def user_login(request):
    # if request.method == 'POST':
        # form = LoginForm(request.POST)
        # if form.is_valid():
            # cd = form.cleaned_data
            # user = authenticate(username=cd['username'], password=cd['password'])

            # if user is not None:
                # if user.is_active:
                    # login(request, user)
                    # return HttpResponse('Authenticated successfully')
                # else:
                    # return HttpResponse('Disabled account')
            # else:
                # return HttpResponse('Invalid login')
    # else:
        # form = LoginForm()
    # return render(request, 'account/login.html', {'form':form})


class ChatRoomView(View):

    def get(self, request):
        chat_queryset = ChatMessage.objects.order_by('-created')[:10]
        chat_message_count = len(chat_queryset)
        if chat_message_count > 0:
            first_message_id = chat_queryset[len(chat_queryset)-1].id
        else:
            first_message_id = -1
        previous_id = -1
        if first_message_id != -1:
            try:
                previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by('-pk')[:1][0].id
            except IndexError:
                previous_id = -1
        chat_messages = reversed(chat_queryset)

        return render(request, 'chat/chatroom.html', {'section': 'chatroom','chat_messages': chat_messages, 'first_message_id': first_message_id})
