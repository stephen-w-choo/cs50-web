from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auction", views.create_auction, name = "create_auction"),
    path("listing/<int:auction_id>", views.listing, name = "listing"),
    path("comment/<int:auction_id>", views.listing, name="comment"),
    path("watch", views.watch, name="watchlist"),
    path("watch/<int:auction_id>", views.watch, name="watch"), 
    path("bid", views.bid, name = "bid"),
    path("close_auction/<int:auction_id>", views.close_auction, name="close_auction")
]
