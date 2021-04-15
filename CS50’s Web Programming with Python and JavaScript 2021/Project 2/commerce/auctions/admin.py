from django.contrib import admin
from .models import User, Bid, Coment, Category, Auction_listing

# Register your models here.

admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Coment)
admin.site.register(Auction_listing)