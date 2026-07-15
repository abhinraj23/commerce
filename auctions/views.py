from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q

from .models import *
from .forms import *

def index(request,message=None,cat=None):
    message=request.GET.get("message")
    cat=request.GET.get("cat")
    if cat:
    	r_cat=category.objects.get(pk=cat)
    else:
    	r_cat=None
    lists=listing.objects.all()
    return render(request, "auctions/index.html",{"lists":lists,"message":message,"cat":r_cat})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
	if request.method != "POST":
		form=create_form()
		return render(request,"auctions/create.html",{"form":form})
	else:
		form=create_form(request.POST)
		if form.is_valid():
			item=form.cleaned_data["item_name"]
			description=form.cleaned_data["description"]
			price=form.cleaned_data['price']
			category=form.cleaned_data['category_name']
			expiry=form.cleaned_data["last_date"]
			print("first")
			image=form.cleaned_data["image"]
			print("second")
			new=listing(owner_name=request.user,item_name=item,description=description,price=price,category_name=category,last_date=expiry,image=image)
			new.save()
			print("third")
			return HttpResponseRedirect(reverse('auctions:index'))
			

def details(request,pk,message=" ",type=" "):
	message=request.GET.get("message")
	type=request.GET.get("type")
	obj=listing.objects.get(pk=pk)
	c_user=request.user
	comments=obj.comments.all()
	highest=bid.objects.filter(item=obj).order_by('-bid_price').first()
	if obj in c_user.watchlist.all():
		button=False
	else:
		button=True
	try:
	
		c_bid=bid.objects.get(Q(item=obj) & Q(bidder=c_user))
		if c_bid is not None:
			hide=1
			c_bid
			if c_bid.bid_price<highest.bid_price:
				repeat=1
			else:
				repeat=0	
			return render(request,"auctions/details.html",{"object":obj,"button":button,"highest":highest,"repeat":repeat,"hide":hide,"c_bid":c_bid,"type":type,"message":message,"comments":comments})
		return render(request,"auctions/details.html",{"object":obj,"button":button,"highest":highest,"message":message,"type":type,"comments":comments})
	except (AttributeError,bid.DoesNotExist) as e:
		print(f"Error: {e}")
		return render(request,"auctions/details.html",{"object":obj,"highest":highest,"button":button,"message":message,"type":type,"comments":comments})


def add_wl(request,id,sts):
	c_user=request.user
	obj=listing.objects.get(pk=id)
	if sts==1:
		c_user.watchlist.add(obj)
	else:
		c_user.watchlist.remove(obj)
	return HttpResponseRedirect(reverse('auctions:details',args=[obj.pk]))


def bids(request,pk):
	obj=listing.objects.get(pk=pk)
	bidder=request.user
	price=request.POST['price']
	highest=bid.objects.filter(item=obj).order_by('-bid_price').first()
	if obj in bidder.watchlist.all():
		button=False
	else:
		button=True
	if float(price)<obj.price:
		message="The bid must be greater than base price"
		type="failed"
		return HttpResponseRedirect(f'/details/{obj.pk}/?message={message}&type={type}')
	if highest is not None:
			if float(price)<=highest.bid_price:
				message="The bid must be greater than current higher bid"
				type="failed"
				return HttpResponseRedirect(f'/details/{obj.pk}/?message={message}&type={type}')
			else:
				new=bid(item=obj,bidder=bidder,bid_price=float(price))
				new.save()
				message="Your bidding is Successfull"
				type="success"
				return HttpResponseRedirect(f'/details/{obj.pk}/?message={message}&type={type}')
	else:
				new=bid(item=obj,bidder=bidder,bid_price=float(price))
				new.save()
				message="Your bidding is Successfull"
				type="success"
				return HttpResponseRedirect(f'/details/{obj.pk}/?message={message}&type={type}')
		

def delete_bid(request,id):
		d_bid=bid.objects.get(pk=id)
		obj=d_bid.item
		d_bid.delete()
		type="success"
		message="Your bid is deleted succesfully"
		print(2)
		return HttpResponseRedirect(f'/details/{obj.pk}/?message={message}&type={type}')
		
	

def edit_bid(request,id):
	c_bid=bid.objects.get(pk=id)
	obj=c_bid.item
	highest=bid.objects.filter(item=obj).order_by('-bid_price').first()
	if request.method=="GET":
		return render(request,"auctions/edit_bid.html",{"obj":obj,"c_price":c_bid.bid_price,"high":highest,"c_bid":c_bid})
	else:
		new_price=float(request.POST['new_price'])
		if new_price>highest.bid_price:
			c_bid.delete()
			new=bid(item=obj,bidder=request.user,bid_price=new_price)
			new.save()
			message="Your new bid is places.you have the highest bid now"
			type="success"
			return HttpResponseRedirect(f"/details/{obj.pk}/?message={message}&type={type}")
		else:
			message=f"Your bid must be greater than current highest bid({highest.bid_price})"
			return render(request,"auctions/edit_bid.html",{"obj":obj,"c_price":c_bid.bid_price,"high":highest,"c_bid":c_bid,"message":message})

def edit_listing(request,id):
	obj=listing.objects.get(pk=id)
	highest=bid.objects.filter(item=obj).order_by('-bid_price').first()
	if request.method == "GET":
		form=create_form(instance=obj)
		return render(request,"auctions/edit_listing.html",{"obj":obj,"form":form,'highest':highest})
	else:
		form=create_form(request.POST,instance=obj)
		if form.is_valid():
			form.save()
			message="The listing is updated successfully"
			type="success"
			return HttpResponseRedirect(f"/details/{obj.pk}/?message={message}&type={type}")


def delete_listing(request,id):
		d_listing=listing.objects.get(pk=id)
		print(1)
		d_listing.delete()
		print(2)
		message="Your listing is deleted succesfully"
		print(3)
		return HttpResponseRedirect(f'/?message={message}')
		

def close_auction(request,id):
	print(1)
	obj=listing.objects.get(pk=id)
	highest=bid.objects.filter(item=obj).order_by('-bid_price').first().bidder
	print(2)
	obj.winner=highest
	print(3)
	obj.status=False
	print(4)
	obj.save()
	message=f"Successfully sold the item to {highest}"
	type="success"
	return HttpResponseRedirect(f"/details/{obj.pk}/?message={message}&type={type}")
	
def my_bids(request):
	c_user=request.user
	bids=c_user.bids.all()
	return render(request,"auctions/my_bids.html",{"bids":bids})
	
def my_listings(request):
	c_user=request.user
	c_listings=c_user.items.all()
	highest={}
	for i in c_listings:
		bids=i.bids.all()
		highest[i]=bids.order_by("-bid_price").first()

	return render(request,"auctions/my_listings.html",{"listings":c_listings,"highest":highest})


def add_comment(request,id):
	obj=listing.objects.get(pk=id)
	c_user=request.user
	topic=request.POST['comment']
	new_c=comment(username=c_user,topic=topic,item=obj)
	new_c.save()
	return HttpResponseRedirect(reverse('auctions:details',args=[obj.pk]))

def categories(request):
	cat=category.objects.all()
	return render(request,"auctions/categories.html",{"cat":cat})
	
def watchlist(request):
	c_user=request.user
	wl=c_user.watchlist.all()
	return render(request,"auctions/watchlist.html",{"wl":wl})