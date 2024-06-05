from django.contrib import admin
from django.urls import path
from fairytale import views
from fairytale.views import add_to_favorites

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('profile/', views.user_profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('create_story/', views.create_story, name='create_story'),
    path('edit_story/<int:story_id>/', views.edit_story, name='edit_story'),
    path('delete_story/<int:story_id>/', views.delete_story, name='delete_story'),
    path('add_to_favorites/', add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
]
