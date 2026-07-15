from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.apps import apps


class User(AbstractUser):
    watchlist=models.ManyToManyField('listing',blank=True,related_name="watchers")
    class Meta:
    	verbose_name_plural = "user"
    def __str__(self):
    	return f"{self.username}"

class category(models.Model):
	name=models.CharField(max_length=50)
	
	def __str__(self):
		return f"{self.name}"
	
	class Meta:
		verbose_name_plural = "category"

class listing(models.Model):
	owner_name=models.ForeignKey('User',on_delete=models.CASCADE,related_name="items")
	category_name=models.ForeignKey('category',on_delete=models.PROTECT,related_name="items")
	item_name=models.CharField(max_length=26)
	description=models.TextField()
	price=models.FloatField()
	status=models.BooleanField(default=True)
	last_date=models.DateField(default=date.today)
	image=models.URLField(max_length=1000,default="",null=True)
	winner=models.ForeignKey('User',on_delete=models.CASCADE,related_name="winnings",null=True)
	
	
	def __str__(self):
		return f"{self.item_name} by ({self.owner_name})"
	
	class Meta:
		verbose_name_plural = "listings"

class bid(models.Model):
	item=models.ForeignKey('listing',on_delete=models.CASCADE,related_name="bids")
	bidder=models.ForeignKey('User',on_delete=models.CASCADE,related_name='bids')
	bid_price=models.FloatField()
	
	def __str__(self):
		return f"bid by {self.bidder} for {self.item} with {self.bid_price}"
	
	class Meta:
		verbose_name_plural = "bid"

class comment(models.Model):
	item=models.ForeignKey('listing',on_delete=models.CASCADE,related_name="comments")
	username=models.ForeignKey('User',on_delete=models.PROTECT,related_name="comments")
	topic=models.TextField(max_length=1000)
	c_date=models.DateField(default=date.today)
	
	def save(self,*args,**kwargs):
		if not self.c_date:
			self.c_date=date.today()
		super().save(*args,**kwargs)
	
	class Meta:
		verbose_name_plural = "comment"
	
	def __str__(self):
		return f"comment by{self.username} in {self.item}"