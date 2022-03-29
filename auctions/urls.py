from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories/<str:category_type>", views.category, name="category"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("comment", views.comment, name="comment"),
    path("close", views.close_auction, name="close_auction"),
]


