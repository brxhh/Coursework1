from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Story(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    is_read = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Story, related_name='favorited_by')
    unread = models.ManyToManyField(Story, related_name='unread_by')
    def get_favorite_stories(self):
        return self.favorites.all()

    def get_top_stories(self):
        return Story.objects.annotate(num_favorites=Count('favorited_by')).order_by('-num_favorites')

    def get_unread_stories(self):
        return Story.objects.filter(is_read=False)

    def __str__(self):
        return self.title