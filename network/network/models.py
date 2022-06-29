from io import open_code
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Relationship(models.Model):
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed_by = models.ForeignKey(User, related_name="followed_by", on_delete=models.CASCADE)

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_post")
    content = models.TextField(blank=False)
    time = models.DateTimeField()
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True, default=None)