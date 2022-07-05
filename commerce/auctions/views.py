import re
from xmlrpc.client import DateTime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django import forms
from . import models
import datetime

from .models import User

def index(request):
    return render(request, "auctions/index.html", {
        "active_listings" : models.AuctionItem.objects.all(),
        "id" : request.user.username
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_auction(request):
    class CreateAuction(forms.ModelForm):
        class Meta: 
            model = models.AuctionItem
            fields = [
                "title",
                "currentprice",
                "description",
                "image",
                "item_type"
            ]
            labels = {
            'currentprice': ('Opening bid'),
            }

            
   
    if request.method == "GET":
        return render(request, "auctions/create_auction.html", {
            "form": CreateAuction()
        })
    
    if request.method == "POST":
        auction_form = CreateAuction(request.POST, request.FILES)
        if auction_form.is_valid():
            auction_form = auction_form.save(commit=False)
            auction_form.owner = request.user
            auction_form.save()
            return redirect("index")
        return HttpResponse(auction_form)

class CommentForm(forms.Form):
    comment= forms.CharField(widget=forms.Textarea)

class AuctionBid(forms.ModelForm):
    class Meta: 
        model = models.AuctionBid
        fields = [
            "auction_item",
            "bid"
        ]
        labels = {
        "bid": ('Bid'),
        }

        widgets = {
            "auction_item": forms.HiddenInput()
        }

def listing(request, auction_id):
    if request.method == "GET":
        listing = get_object_or_404(models.AuctionItem, id=auction_id)

        highestbidder = False

        if request.user.id == listing.owner.id:
            status = "owner"
            if listing.sold == True:
                status = "ownersold"
        elif listing.sold == True:
            status = "sold"
            if request.user.id == listing.highest_bidder.id:
                status = "winner"
        elif request.user.is_authenticated:
            status = "open"
            if listing.highest_bidder:
                if request.user.id == listing.highest_bidder.id:
                    highestbidder = True
        else:
            status = "guest"

        if request.user in listing.watching.all():
            watching = True
        else:
            watching = False
      
        comments = models.AuctionComment.objects.filter(item=auction_id)
        return render(request, "auctions/listing.html", {
            "login": login,
            "item": listing,
            "comments": comments,
            "commentform": CommentForm(),
            "bid_form": AuctionBid(initial={"auction_item": auction_id}),
            "auction_id": auction_id,
            "status": status,
            "highestbidder": highestbidder,
            "watching": watching
        })

    if request.method == "POST":
        comment = CommentForm(request.POST)
        if comment.is_valid():
            item_name = models.AuctionItem.objects.get(id=auction_id)
            comment_body = comment.cleaned_data["comment"]
            time = datetime.datetime.now()
            c = models.AuctionComment(item=item_name, user=request.user, comment=comment_body, time = time)
            c.save()
            return redirect("listing", auction_id = auction_id)  

def watch(request, auction_id=None):
    user_id = request.user

    if request.method == "GET":
        current_user = models.User.objects.get(id=request.user.id)
        watchlist= current_user.watchlist.all()
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist
        })

    if request.method == "POST":
        auction_item = models.AuctionItem.objects.get(pk=auction_id)
        if auction_item.watching.filter(pk=user_id.id).exists():
            auction_item.watching.remove(user_id.id)
        else:
            auction_item.watching.add(user_id.id)
        return redirect("listing", auction_id = auction_id)

def bid(request):
    if request.method == "POST":
        bid_data = AuctionBid(request.POST)
        
        if bid_data.is_valid():
            current_item = bid_data.cleaned_data["auction_item"]
            if bid_data.cleaned_data["bid"] > current_item.currentprice and current_item.sold == False:
                current_item.currentprice = bid_data.cleaned_data["bid"]
                current_item.highest_bidder = request.user
                current_item.save()
                bid_data = bid_data.save(commit = False)
                bid_data.bidder = request.user
                bid_data.time = datetime.datetime.now()
                bid_data.save()
                return redirect("listing", auction_id = bid_data.auction_item.id)
            return render(request, "auctions/error.html", {
                "error": "Bid invalid, please input a price higher than current bid"
                })

def close_auction(request, auction_id):
    auction_item = get_object_or_404(models.AuctionItem, id=auction_id)
    if request.user == auction_item.owner:
        auction_item.sold = True
        auction_item.save()
    return redirect("listing", auction_id = auction_item.id)


def categories(request):
    all_items = models.AuctionItem.objects.all()
    categories= set()
    for item in all_items:
        categories.add(item.item_type)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, item_category):
    all_items = models.AuctionItem.objects.all()
    item_list = []
    for item in all_items:
        if item.item_type == item_category:
            item_list.append(item)
    return render(request, "auctions/category.html", {
        "item_list": item_list
    })