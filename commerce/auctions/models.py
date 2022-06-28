from email.mime import image
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionItem(models.Model):
    title = models.CharField(max_length = 60)
    currentprice = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.TextField()
    image = models.URLField(default = None, blank = True)
    item_type = models.CharField(max_length = 200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    watching = models.ManyToManyField(User, blank = True, related_name="watchlist")
    sold = models.BooleanField(default = False)
    highest_bidder = models.ForeignKey(User, null= True, on_delete=models.CASCADE, related_name="highest_bidder")

class AuctionComment(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True)
    comment = models.TextField()
    time = models.DateTimeField()

class AuctionBid(models.Model):
    auction_item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, blank = True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits = 10, decimal_places = 2)
    time = models.DateTimeField()
