from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("shoes", views.shoes, name="shoes"),
    path("clothing", views.clothing, name="clothing"),
    path("electronics", views.electronics, name="electronics"),
    path("smartphones", views.smartphones, name="smartphones"),
    path("success", views.success, name="success"),
    path("error", views.error, name="error"),
    path("comments/<int:auc_id>/", views.comment, name="comments"),
    path("active_listings", views.listings, name="active_listings"),
    path("watchlist_add/<int:auc_id>/", views.watchlist_add, name="watchlist_add"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("close_auction/<int:auc_id>/", views.close, name="close"),
    path("active_listings/<int:auc_id>/", views.list_item, name="details"),
]
