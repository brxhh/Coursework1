from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
import json
from .forms import UserRegistrationForm, StoryForm
from .models import UserProfile, Story


def home(request):
    popular_stories = Story.objects.all().order_by('-likes')
    return render(request, 'home.html', {'popular_stories': popular_stories})

@login_required
def user_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    favorites = user_profile.get_favorite_stories()
    top_stories = user_profile.get_top_stories()
    unread = user_profile.get_unread_stories()
    return render(request, 'profile.html', {'favorites': favorites, 'top_stories': top_stories, 'unread': unread})


@login_required
@require_POST
def add_to_favorites(request):
    try:
        data = json.loads(request.body)
        story_id = data.get('story_id')
        if not story_id:
            return JsonResponse({'success': False, 'error': 'story_id not provided'})

        story = Story.objects.get(id=story_id)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        if story in user_profile.favorites.all():
            user_profile.favorites.remove(story)
            added = False
        else:
            user_profile.favorites.add(story)
            added = True

        user_profile.save()
        return JsonResponse({'success': True, 'added': added})
    except Story.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Story does not exist'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'})

@login_required
def remove_from_favorites(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        story_id = data.get('story_id')
        user_profile = request.user.userprofile
        if story_id:
            story = Story.objects.filter(pk=story_id).first()
            if story:
                user_profile.favorites.remove(story)
                return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Неправильне ім'я користувача або пароль."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@user_passes_test(lambda u: u.is_superuser)
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')
    else:
        form = StoryForm()
    return render(request, 'create_story.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    if request.method == 'POST':
        form = StoryForm(request.POST, instance=story)
        if form.is_valid():
            form.save()
            return redirect('admin_profile')
    else:
        form = StoryForm(instance=story)
    return render(request, 'edit_story.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_story(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    if request.method == 'POST':
        story.delete()
        return redirect('admin_profile')
    return render(request, 'delete_story.html', {'story': story})

@user_passes_test(lambda u: u.is_superuser)
def admin_profile(request):
    stories = Story.objects.all()
    return render(request, 'admin_profile.html', {'stories': stories})
