from email.mime import image
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionItem(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.owner.id, filename)

    def __str__(self):
        return f"{self.title} sold by ({self.owner})"
    title = models.CharField(max_length = 60)
    currentprice = models.DecimalField(max_digits = 10, decimal_places = 2)
    description = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, null = True, blank= True,  default=None)
    item_type = models.CharField(max_length = 200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    watching = models.ManyToManyField(User, null = True, blank= True,  default=None, related_name="watchlist")
    sold = models.BooleanField(default = False)
    highest_bidder = models.ForeignKey(User, null = True, blank= True,  default=None, on_delete=models.CASCADE, related_name="highest_bidder")

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

class Category(models.Model):
    pass