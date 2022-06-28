from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.AuctionItem)
admin.site.register(models.AuctionComment)
admin.site.register(models.AuctionBid)