from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from .util import bids, bids_reference, list_categories, auction_current_bid, watchlist, winner, auction_creator_close
from django import forms

from .models import User, Bid, Auction_listing, Coment, Category


def index(request):
    if request.method=="GET":
        return render(request, "auctions/index.html", {
            "auctions": Auction_listing.objects.filter(active_status=True).order_by("-created_at"),
            "bids": bids(),
            "bids_reference": bids_reference()
        })
    else:
        return render(request, "auctions/index.html")


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

def create(request):

    class NewAuctionForm(forms.Form):
        categories = tuple(list_categories())
        title = forms.CharField(label="Title", max_length=128, required=True,widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ))
        description = forms.CharField(label="Description", max_length=1024, required=True,widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '4',
            }
        ))
        category = forms.ChoiceField(choices=categories, required=True, widget=forms.Select(
            attrs={
                'class':'form-control',
            }
        ))
        startind_bid = forms.IntegerField(label="Starting Bid", min_value=0, required=True, widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': '$'
            }
        ))
        image_link = forms.URLField(label="Image Link", max_length=4096, required=False, widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ))

    if request.method == "GET":
        if User.is_authenticated:
            return render(request, "auctions/create.html",{
                "form": NewAuctionForm()
            })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["image_link"] == '':
                img_link = 'http://www.plasson.com.br/livestock/images/image-not-found.jpg'
            else:
                img_link = form.cleaned_data["image_link"]
            auction = Auction_listing(title=form.cleaned_data["title"], description=form.cleaned_data["description"], image_link=img_link, startind_bid=form.cleaned_data["startind_bid"], created_at=timezone.now(), active_status=True, category= Category.objects.filter(id=form.cleaned_data["category"])[0], created_by=request.user)
            auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": NewAuctionForm(),
                "message": form.errors
            })


def close(request, auction_id):
    auction_info = Auction_listing.objects.get(pk=auction_id)
    auction_info.active_status = False
    auction_info.save()
    return HttpResponseRedirect(reverse("page", args=(auction_id,)))


def page(request, auction_id):

    class PlaceBidForm(forms.Form):
        value = forms.IntegerField(label="Value",min_value=auction_current_bid(auction_id), required=True,widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Place a Bid',
            }
        ))

    class PlaceComentForm(forms.Form):
        text = forms.CharField(label="Coment", max_length=1024, required=True,widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows': '4',
                'placeholder':'Place a Coment'
            }
        ))

    auction_info = Auction_listing.objects.get(pk=auction_id)
    coments = Coment.objects.filter(auction=auction_id).order_by("-timestamp")
    watchlist_info = watchlist(request.user,auction_id)

    if request.method == "GET":
        return render(request, "auctions/page.html", {
            "auction": auction_info,
            "coments": coments,
            "bid": auction_current_bid(auction_id),
            "place_bid": PlaceBidForm(),
            "place_coment": PlaceComentForm(),
            "watchlist_info": watchlist_info,
            "winner": winner(auction_id, request.user),
            "creator": auction_creator_close(auction_id, request.user)
        })
    else:
        if "PlaceBid" in request.POST:
            bidform = PlaceBidForm(request.POST)
            if bidform.is_valid():
                bid = Bid(value=bidform.cleaned_data["value"], timestamp=timezone.now(), auction=Auction_listing.objects.get(pk=auction_id), created_by=request.user)
                bid.save()
                return render(request, "auctions/page.html", {
                    "auction": auction_info,
                    "coments": coments,
                    "bid": auction_current_bid(auction_id),
                    "place_bid": PlaceBidForm(),
                    "place_coment": PlaceComentForm(),
                    "message": "Bid Placed",
                    "watchlist_info": watchlist_info,
                    "winner": winner(auction_id, request.user),
                    "creator": auction_creator_close(auction_id, request.user)
                })
            else:
                return render(request, "auctions/page.html", {
                    "auction": auction_info,
                    "coments": coments,
                    "bid": auction_current_bid(auction_id),
                    "place_bid": PlaceBidForm(),
                    "place_coment": PlaceComentForm(),
                    "message": bidform.errors,
                    "watchlist_info": watchlist_info,
                    "winner": winner(auction_id, request.user),
                    "creator": auction_creator_close(auction_id, request.user)
                })
        elif "Coment" in request.POST:
            comentform = PlaceComentForm(request.POST)
            if comentform.is_valid():
                coment = Coment(text = comentform.cleaned_data["text"],auction=Auction_listing.objects.get(pk=auction_id), timestamp=timezone.now(), created_by=request.user)
                coment.save()
                return render(request, "auctions/page.html", {
                    "auction": auction_info,
                    "coments": coments,
                    "bid": auction_current_bid(auction_id),
                    "place_bid": PlaceBidForm(),
                    "place_coment": PlaceComentForm(),
                    "message": "Coment placed. =)",
                    "watchlist_info": watchlist_info,
                    "winner": winner(auction_id, request.user),
                    "creator": auction_creator_close(auction_id, request.user)
                })
            else:
                return render(request, "auctions/page.html", {
                    "auction": auction_info,
                    "coments": coments,
                    "bid": auction_current_bid(auction_id),
                    "place_bid": PlaceBidForm(),
                    "place_coment": PlaceComentForm(),
                    "message": comentform.errors,
                    "watchlist_info": watchlist_info,
                    "winner": winner(auction_id, request.user),
                    "creator": auction_creator_close(auction_id, request.user)
                })
        elif "Watchlistadd" in request.POST:
            auction_info.watchlist.add(request.user)
            watchlist_info = watchlist(request.user, auction_id)
            return render(request, "auctions/page.html", {
                "auction": auction_info,
                "coments": coments,
                "bid": auction_current_bid(auction_id),
                "place_bid": PlaceBidForm(),
                "place_coment": PlaceComentForm(),
                "watchlist_info": watchlist_info,
                "winner": winner(auction_id, request.user),
                "creator": auction_creator_close(auction_id, request.user)
            })

        else:
            auction_info.watchlist.remove(request.user)
            watchlist_info = watchlist(request.user, auction_id)
            return render(request, "auctions/page.html", {
                "auction": auction_info,
                "coments": coments,
                "bid": auction_current_bid(auction_id),
                "place_bid": PlaceBidForm(),
                "place_coment": PlaceComentForm(),
                "watchlist_info": watchlist_info,
                "winner": winner(auction_id, request.user),
                "creator": auction_creator_close(auction_id, request.user)
            })

def user_watchlist (request):
    user = User.objects.get(username=request.user)
    user_watchlist = user.users_watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist,
        "bids": bids(),
        "bids_reference": bids_reference()
    })


def categories (request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category (request, category_id):
    return render(request, "auctions/category.html", {
        "auctions":Auction_listing.objects.filter(category=category_id),
        "bids": bids(),
        "bids_reference": bids_reference(),
        "category": Category.objects.get(id=category_id)
    })