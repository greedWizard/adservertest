from django.urls import path

from .views import Ads, Categories, AdView, CategoryAdsView, UserAds, SearchHistory


urlpatterns = [
    path('ads/', Ads.as_view()),
    path('ads/<int:id>', AdView.as_view()),
    path('ads/by_user/<int:user_id>', UserAds.as_view()),
    path('categories/', Categories.as_view()),
    path('categories/<int:id>', CategoryAdsView.as_view()),
    path('history/', SearchHistory.as_view()),
]