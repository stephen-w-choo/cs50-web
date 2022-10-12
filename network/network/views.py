from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Relationship, Post
from .forms import New_Post

import datetime


def index(request):
    list_all = Post.objects.all().order_by("-time")
    return render(request, "network/index.html", {
        "post_form": New_Post,
        "list_all": list_all
    })

def make_post(request):
    received_post = New_Post(request.POST)
    if request.method == "POST":
        if received_post.is_valid():
            received_post = received_post.save(commit=False)
            received_post.poster = request.user
            received_post.time = datetime.datetime.now()
            received_post.save()
            return redirect("index")

def profile(request, profile_id):
    # get all posts by user
    user_posts = Post.objects.filter(poster_id=profile_id)
    following = False
    if Relationship.objects.filter(user_id=request.user, following_user_id=User.objects.get(pk=profile_id)).exists():
        following = True
    return render(request, "network/profile.html", {
        "user_posts": user_posts,
        "following": following
    })

def follow(request, profile_id):
    # follow another user
    current_relationship = Relationship.objects.filter(user_id=request.user, following_user_id=User.objects.get(pk=profile_id))
    # check if already following
    if current_relationship.exists():
        # unfollow and return early
        current_relationship.delete()
        return redirect("profile", profile_id=profile_id)

    new_relationship = Relationship(user_id=request.user, following_user_id=User.objects.get(pk=profile_id))
    new_relationship.save()
    return redirect("profile", profile_id=profile_id)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

