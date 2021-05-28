from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.contrib import messages
from .forms import Comment_form, Create_form,Bid_form
from .models import Auction_listings, Bids,User,Comments, Watchlist



def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return HttpResponseRedirect(reverse("active_listings"))


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
    return HttpResponseRedirect(reverse("login"))

@login_required
def create_listing(request):
    if request.method == "POST":
        # get all form data
        form = Create_form(request.POST or None)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            price = form.cleaned_data["price"]
            date = form.cleaned_data["date_created"]
            category = form.cleaned_data["category"]
            user = request.user
            # save to Auction_listings table
            auc = Auction_listings(title=title,
                    description=description,
                    image=image,price=price,
                    date_created=date,
                    category=category,
                    creator = user
                    )

            # if the the image length is less than or equal to 200, save else, give the error
            if len(image) <= 200:
                auc.save()
                return HttpResponseRedirect(reverse('success'))
            else:
                message = "URL link exceeds the maximum length of 200"
                return render(request, "auctions/create_listing.html", {
                    "form": Create_form, "message": message
                    })

    else:
        form = Create_form()
    return render(request, "auctions/create_listing.html", {"form": Create_form})

def success(request):
    return render(request, "auctions/success.html")

def error(request):
    return render(request, "auctions/error.html")

@login_required
def categories(request):
    return render(request, "auctions/categories.html")

@login_required
def list_item(request, auc_id):
    if request.method == "POST":
        # get bid form data
        form = Bid_form(request.POST or None)
            
        # if data valid, get data, auc listing id, current user and price
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            object = get_object_or_404(Auction_listings, pk=auc_id)
            item_id = object.id
            price = object.price
            username = request.user
            
            
            # if bid is less than price, give error message
            if bid < price:
                message = "Bid must be more than original price"
                title = get_object_or_404(Auction_listings, pk=auc_id)
                return render(request, "auctions/list.html", { "message": message,
                    "title": title, "cform": Comment_form, "bform": Bid_form})

            # get all bids
            all_bids = Bids.objects.filter(item_id=item_id).values()
            # if there are no bids, save the current bid to the bids table and print message(user won the bid)
            if len(all_bids) == 0:
                b = Bids(
                    user=username,
                    item_id=item_id,
                    bid=bid
                )
                b.save()
                bid_message = "You won the bid!"
                title = get_object_or_404(Auction_listings, pk=auc_id)
                return render(request, "auctions/list.html", { "bid_message": bid_message,
                    "title": title, "cform": Comment_form, "bform": Bid_form})
            
            # loop through all bids. if current bid is greater than old bid or lower. print message accordingly
            for each_bid in all_bids:
                old_bid = each_bid["bid"]
                if bid > old_bid:
                    cmessage = "You won the bid!"
                cmessage = "There's a higher bid"

            # save the bid
            b = Bids(
                    user=username,
                    item_id=item_id,
                    bid=bid
                )
            b.save()
            title = get_object_or_404(Auction_listings, pk=auc_id)
            return render(request, "auctions/list.html", { "bid_message": cmessage,
                    "title": title, "cform": Comment_form, "bform": Bid_form})

    # If method is "GET":
    title = get_object_or_404(Auction_listings, pk=auc_id)
    comments = Comments.objects.filter(listing=auc_id)
    return render(request, "auctions/list.html", {"comments": comments,"title": title, "cform": Comment_form, "bform": Bid_form})


def comment(request, auc_id):
    if request.method == "POST":
        # if comment data is valid, save to comments table
        form = Comment_form(request.POST or None)
        if form.is_valid():
            listing_id = auc_id
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            body = form.cleaned_data["body"]

            com = Comments(
                listing= listing_id,
                name=name,
                email=email,
                body=body
            )

            com.save()
        
            return redirect("details", auc_id)

@login_required
def listings(request):
    listings = Auction_listings.objects.all()
    return render(request, "auctions/active_listings.html", {"listings": listings})

@login_required
def watchlist_add(request, auc_id):
    item = get_object_or_404(Auction_listings, pk=auc_id)
    # Check if the item already exists in that user watchlist
    if Watchlist.objects.filter(user=request.user, item=item.id).exists():
        messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("index"))
        # Get the user watchlist or create it if it doesn't exists
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    # Add the item through the ManyToManyField (Watchlist => item)
    user_list.item.add(item)
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    return redirect("watchlist")

@login_required
def watchlist(request):
    # list_of_id = Watchlist.objects.filter(user=request.user).values()
    
    watchlist = Watchlist.item.through.objects.all().values()
    list_of_id = []
    for x in watchlist:
        auc_id = x['auction_listings_id']
        list_of_id.append(Auction_listings.objects.get(pk=auc_id))
    print(list_of_id)
    return render(request, "auctions/watchlist.html", {"watchlist": list_of_id})

@login_required
def close(request, auc_id):
    '''
        If request method is post, it will receive the data and change
         the column of that specific item(gotten through the id) and update closed column to 
        True.
    '''
    if request.method == "POST":
        obj = Auction_listings(pk=auc_id)
        obj.closed = True
        obj.save(update_fields=['closed'])
        return redirect("details", auc_id)

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

def shoes(request):
    shoes = Auction_listings.objects.filter(category="sh")
    return render(request, "auctions/shoes.html", {"shoes": shoes})

def clothing(request):
    cl = Auction_listings.objects.filter(category="cl")
    return render(request, "auctions/clothing.html", {"clothes": cl})

def electronics(request):
    el = Auction_listings.objects.filter(category="el")
    return render(request, "auctions/electronics.html", {"elects": el})

def smartphones(request):
    sm = Auction_listings.objects.filter(category="sm")
    return render(request, "auctions/smartphone.html", {"phones": sm})
