from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	user_id = models.AutoField(primary_key=True)

class category(models.Model):
	name=models.CharField(max_length=50)

class listing(models.Model):
	owner_name=models.ForeignKey(User,on_delete=models.CASCADE,related_name="items")
	category_name=models.ForeignKey(category,on_delete=models.PROTECT,related_name="items")
	item_name=models.CharField(max_length=26)
	description=models.TextField()
	price=models.FloatField()
	status=models.BooleanField(default=True)
	duration=models.DurationField()

class bid(models.Model):
	item=models.ManyToManyField(listing,related_name="bids")
	bidder=models.ManyToManyField(User,related_name='bids')
	bid_price=models.FloatField()

class comment(models.Model):
	topic=models.ManyToManyField(listing,related_name="comments")
	user=models.ManyToManyField(User,related_name="comments")
	
