from django.urls import path

from .views import Categories, AdView, CategoryAdsView, UserAds, Ads, SearchHistory, FavoriteAdsView, FavoriteSellersView, TagsView


urlpatterns = [
    path('ads/', Ads.as_view()),
    path('ads/<int:id>', AdView.as_view()),
    path('ads/by_user/<int:user_id>', UserAds.as_view()),
    path('categories/', Categories.as_view()),
    path('categories/<int:id>', CategoryAdsView.as_view()),
    path('history/', SearchHistory.as_view()),
    path('tags/', TagsView.as_view()),
    path('favorite_sellers/', FavoriteSellersView.as_view()),
    path('favorite_ads/', FavoriteAdsView.as_view()),
]