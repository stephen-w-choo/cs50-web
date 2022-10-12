from io import open_code
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Relationship(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"


class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_post")
    content = models.TextField(blank=False)
    time = models.DateTimeField()
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True, default=None)