from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import User, Relationship, Post
from .forms import New_Post

import datetime


def index(request):
    list_all = Post.objects.all().order_by("-time")

    # use paginator to split posts into pages
    paginator = Paginator(list_all, 10)

    # check if the request includes a page number
    page_number = request.GET.get('pages')
    # if not, set page number to 1
    print(request.GET)
    if page_number is None:
        page_number = 1
    # get the page
    print(page_number)
    page_obj = paginator.get_page(page_number)
    # get the total number of pages
    total_pages = paginator.num_pages
    print(page_obj.has_next())

    return render(request, "network/index.html", {
        "post_form": New_Post,
        "page_posts": page_obj,
        "total_pages": total_pages
    })

def make_post(request):
    received_post = New_Post(request.POST)
    if request.method == "POST":
        # check that the poster and the user are the same

        if received_post.is_valid():
            received_post = received_post.save(commit=False)
            received_post.poster = request.user
            received_post.time = datetime.datetime.now()
            received_post.save()
            return redirect("index")

def posts(request, post_id):
    # get the post
    if request.method == "GET":
        post = get_object_or_404(Post, pk=post_id)
        # check if the user has already liked the post
        if request.user in post.liked_by.all():
            # unlike the post
            post.liked_by.remove(request.user)
            return JsonResponse(
                {
                    "message": "Post unliked successfully.",
                    "likes": post.liked_by.count()
                },
                status=201
            )
        else:
            # like the post
            post.liked_by.add(request.user)
            return JsonResponse(
                {
                    "message": "Post liked successfully.",
                    "likes": post.liked_by.count()
                },
                status=201
            )

    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        # check if the user is the poster
        if post.poster != request.user:
            return JsonResponse({"message": "Forbidden"}, status=401)

        if "content" in request.POST:
            # edit the content
            post.content = request.POST["content"]
            post.save()
            return JsonResponse(
                {
                    "content": post.content,
                    "message": "Post updated successfully."
                },
                status=201
            )
        return JsonResponse({"message": "Unsuccessful"}, status=201)


def profile(request, profile_id):
    # get all posts by user
    user_posts = Post.objects.filter(poster_id=profile_id).order_by("-time")
    following = False
    self_profile = False

    # check if the current user is the profile user
    if profile_id == request.user.id:
        self_profile = True

    # check if the current user is following the profile user
    current_relationship = Relationship.objects.filter(user_id=request.user, following_user_id=User.objects.get(pk=profile_id))
    if current_relationship.exists():
        following = True

    # get the number of followers
    n_followers = Relationship.objects.filter(following_user_id=profile_id).count()
    print(n_followers)
    # get the number that the user is following
    n_following = Relationship.objects.filter(user_id=profile_id).count()


    return render(request, "network/profile.html", {
        "user_posts": user_posts,
        "following": following,
        "self_profile": self_profile,
        "n_following": n_following,
        "n_followers": n_followers
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

def following(request):
    # get all posts by users that the current user follows
    user_following_ids = request.user.following.all().values("following_user_id")
    posts = Post.objects.filter(poster_id__in=user_following_ids).order_by("-time")
    return render(request, "network/following.html", {
        "following_posts": posts
    })

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
