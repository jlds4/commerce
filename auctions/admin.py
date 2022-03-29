from django.contrib import admin
from .models import AuctionListing, Bid, ListingComment, WatchlistItem, User

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(ListingComment)
admin.site.register(WatchlistItem)
admin.site.register(User)
