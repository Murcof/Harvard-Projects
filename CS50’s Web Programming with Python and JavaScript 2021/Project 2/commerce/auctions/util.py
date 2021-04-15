from .models import User, Bid, Auction_listing, Coment, Category
from django.db.models import Max

def bids():
    auctions = Auction_listing.objects.filter(active_status=True).order_by("-created_at")
    currentbids = []
    for k in auctions:
        query = Bid.objects.filter(auction = k.id).order_by('-value')
        try:
            currentbids.append(query[0])
        except:
            pass
    return currentbids

def bids_reference():
    #additional info to the bids function
    bido = bids()
    list=[]
    for bid in bido:
        list.append(bid.auction.id)
    return list

def list_categories():
    #function primarilly used to feed create auction form
    list = []
    for category in (Category.objects.all()):
        in_list = []
        in_list.append(category.id)
        in_list.append(category.name)
        list.append(in_list)
    return list

def auction_current_bid(auction):
    try:
        result = Bid.objects.filter(auction=auction).order_by('-value')[0].value
    except:
        result = Auction_listing.objects.filter(id=auction)[0].startind_bid
    return result

def watchlist(user, auction_id):
    auction = Auction_listing.objects.get(id=auction_id)
    if user in auction.watchlist.all():
        return True
    else:
        return False

def winner(auction, user):
    auction_info = Auction_listing.objects.filter(id=auction)[0]
    try:
        verify_bid = Bid.objects.filter(auction=auction).order_by('-value')[0]
        if (verify_bid.created_by == user and auction_info.active_status == False and auction_info.created_by != user):
            return True
        else:
            return False
    except:
        return False


def auction_creator_close(auction, user):
    auction_info = Auction_listing.objects.filter(id=auction)[0]
    if (auction_info.created_by == user and auction_info.active_status == True):
        return True
    else:
        return False