from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.middleware.csrf import get_token
from .models import User, AuctionListing, Bid, ListingComment, WatchlistItem


def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
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


def listing(request, listing_id):
    listing = get_listing(request, listing_id)
    bid = get_bid(request, listing)
    comments = get_comments(request, listing)
    on_watchlist = get_watchlist_status(request, listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid": bid,
        "on_watchlist": on_watchlist,
        "comments": comments
    })


@login_required
def watchlist(request):
    if request.method == "POST":
        listing = AuctionListing.objects.get(id=int(request.POST["listing"]))
        watchlist_item = WatchlistItem(listing=listing, user=request.user)
        watchlist_item.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing.id}))
    watchlist_listings = WatchlistItem.objects.filter(user=request.user)
    listings = []
    for item in watchlist_listings:
        listings.append(item.listing)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def comment(request):
    comment_new = request.POST["comment_new"]
    listing = AuctionListing.objects.get(id=int(request.POST["listing_comment"]))
    comm = ListingComment(listing=listing, user=request.user, content=comment_new, date=timezone.now())
    comm.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing.id}))


def close_auction(request):
    listing = AuctionListing.objects.get(id=int(request.POST["listing_close"]))
    if listing.currentBid_id:
        listing.winner = Bid.objects.get(id=listing.currentBid_id).user
    listing.status = "Finished"
    listing.save(update_fields=["winner", "status"])
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing.id}))


def remove_watchlist(request):
    listing = AuctionListing.objects.get(id=int(request.POST["listing"]))
    item = WatchlistItem.objects.get(listing=listing, user=request.user)
    item.delete()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing.id}))


def bid(request, listing_id):
    bid_value = float(request.POST["bid"])
    listing = AuctionListing.objects.get(id=listing_id)
    if listing.currentBid_id:
        if bid_value > Bid.objects.get(id=listing.currentBid_id).value:
            bid = Bid(listing=listing, user=request.user, value=bid_value, date=timezone.now())
            bid.save()
            listing.currentBid_id = bid.id
            listing.currentBid_value = bid.value
            listing.save(update_fields=["currentBid_id", "currentBid_value"])
        else:
            bid_old = get_bid(request, listing)
            comments = get_comments(request, listing)
            on_watchlist = get_watchlist_status(request, listing)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid": bid_old,
                "on_watchlist": on_watchlist,
                "comments": comments,
                "error_message": "current"
            })
    else:
        if bid_value > listing.startingBid:
            bid = Bid(listing=listing, user=request.user, value=bid_value, date=timezone.now())
            bid.save()
            listing.currentBid_id = bid.id
            listing.currentBid_value = bid.value
            listing.save(update_fields=["currentBid_id", "currentBid_value"])
        else:
            bid_old = get_bid(request, listing)
            comments = get_comments(request, listing)
            on_watchlist = get_watchlist_status(request, listing)
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid": bid_old,
                "on_watchlist": on_watchlist,
                "comments": comments,
                "error_message": "starting"
            })
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing.id}))


def category(request, category_type):
    if category_type:
        try:
            listings = AuctionListing.objects.filter(category=category_type, status="Ongoing")
        except AuctionListing.DoesNotExist:
            raise Http404("Listing not found.")
        return render(request, "auctions/category.html", {
            "category": category_type,
            "listings": listings
        })


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = float(request.POST["bid"])
        image = request.FILES.get("image", False)
        category = request.POST["category"]
        if image:
            listing = AuctionListing(name=title, description=description, user=request.user, startingBid=bid,
                                     category=category, image=image)
            listing.save()
        else:
            listing = AuctionListing(name=title, description=description, user=request.user, startingBid=bid,
                                     category=category)
            listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")


def get_listing(request, listing_id):

    listing = AuctionListing.objects.get(id=listing_id)
    return listing


def get_bid(request, listing):
    if listing.currentBid_id:
        bid = Bid.objects.get(id=listing.currentBid_id)
    else:
        bid = None
    return bid


def get_comments(request, listing):
    comments = ListingComment.objects.filter(listing=listing)
    return comments


def get_watchlist_status(request, listing):
    user = request.user
    if user.is_authenticated:
        try:
            on_watchlist = WatchlistItem.objects.get(listing=listing, user=user)
        except WatchlistItem.DoesNotExist:
            on_watchlist = None
    else:
        on_watchlist = None
    return on_watchlist
