
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("make_post", views.make_post, name="make_post"),
    path("posts/<int:post_id>/like", views.posts, name = "like_post"),
    path("posts/<int:post_id>", views.posts, name = "posts"),
    path("profile/<int:profile_id>", views.profile, name = "profile"),
    path("follow/<int:profile_id>", views.follow, name = "follow"),
    path("following", views.following, name = "following")
]
