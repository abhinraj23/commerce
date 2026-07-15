from django.urls import path

from . import views

app_name='auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("details/<int:pk>/",views.details,name="details"),
    path("add_wl/<int:id>/<int:sts>",views.add_wl,name="add_watchlist"),
    path("bid/<int:pk>",views.bids,name="bids"),
    path("edit_bid/<int:id>",views.edit_bid,name="edit_bid"),
    path("delete_bid/<int:id>",views.delete_bid,name="delete_bid"),
    path("edit_listing/<int:id>",views.edit_listing,name="edit_listing"),
    path("delete_listing/<int:id>",views.delete_listing,name="delete_listing"),
    path("close/<int:id>",views.close_auction,name="close_auction"),
    path("my_bids/",views.my_bids,name="my_bids"),
    path("my_listings",views.my_listings,name="my_listings"),
    path("add_comment/<int:id>",views.add_comment,name="add_comment"),
    path("categories",views.categories,name="categories"),
    path("watchlist",views.watchlist,name="watchlist")
]
