from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Auction_listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    startind_bid = models.IntegerField(validators=[MinValueValidator(0)])
    image_link = models.URLField(max_length=4096, blank=True)
    created_at = models.DateTimeField()
    active_status = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auction_category")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_creator")
    watchlist = models.ManyToManyField(User, blank=True, related_name="users_watchlist")

    def __str__(self):
        return f"{self.title}, category: {self.category}"

class Bid(models.Model):
    value = models.IntegerField(validators=[MinValueValidator(0)])
    timestamp = models.DateTimeField()
    auction = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="auction_bid")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_creator")

    def __str__(self):
        return f"{self.created_by} offered {self.value}, {self.timestamp}"

class Coment(models.Model):
    text = models.CharField(max_length=1024)
    timestamp = models.DateTimeField()
    auction = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="auction_coment")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coment_creator")

    def __str__(self):
        return f"{self.created_by} comented on {self.auction}, {self.timestamp}"
