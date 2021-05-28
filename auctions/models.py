from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from commerce import settings

class User(AbstractUser):
    pass

CATEGORIES = (
    ('sh', 'shoe'),
    ('el', 'electronics'),
    ('cl', 'clothing'),
    ('sm', 'smartphones'),
    ('no', 'None')
)

class Auction_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    image = models.URLField(max_length=200)
    price = models.IntegerField(default=0)
    date_created = models.DateField(auto_now=True, auto_now_add=False)
    category = models.CharField(max_length=30, choices=CATEGORIES, default=CATEGORIES[4][1])
    creator = models.CharField(max_length=30)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"



class Bids(models.Model):
    user = models.CharField(default="",max_length=50)
    item_id = models.IntegerField(default=0) 
    bid = models.IntegerField(max_length=100, default=0)


class Comments(models.Model):
    listing = models.IntegerField(default=0)
    name = models.CharField(max_length=80)
    email = models.EmailField(default="")
    body = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   item = models.ManyToManyField(Auction_listings, related_name="items")
   def __str__(self):
       return f"{self.user.username}: {self.item.auction_listings_id}"

