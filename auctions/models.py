from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctioneer")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    startingBid = models.FloatField()
    currentBid_id = models.IntegerField(blank=True, null=True)
    currentBid_value = models.FloatField(blank=True, null=True)
    statusOptions = [('Ongoing', 'Ongoing'), ('Finished', 'Finished')]
    status = models.CharField(max_length=8, choices=statusOptions, default='Ongoing')
    choicesCategory = [
        ('Toys', 'Toys'),
        ('Clothing', 'Clothing'),
        ('Electronics', 'Electronics'),
        ('Sports', 'Sports'),
        ('General', 'General'),
        ('Jewelry', 'Jewelry'),
        ('Cosmetics', 'Cosmetics'),
        ('Vehicles', 'Vehicles'),
        ('Furniture', 'Furniture'),
        ('Art', 'Art')
    ]
    category = models.CharField(max_length=15, choices=choicesCategory, default='General')
    image = models.ImageField(blank=True, null=True, upload_to='media/')

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    value = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f"${self.value} bid on {self.listing.name} ({self.id})"


class ListingComment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.CharField(max_length=300)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} comment on {self.listing.name}"


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item_on_watchlist")

    def __str__(self):
        return f"{self.listing.name} is on {self.user} watchlist"
