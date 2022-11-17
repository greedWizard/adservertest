from django.urls import path, include
from locations.views import Countries, Cities, States, Regions, Subways, IpData

urlpatterns = [
    path('countries/', Countries.as_view()),
    path('states/', States.as_view()),
    path('cities/', Cities.as_view()),
    path('regions/', Regions.as_view()),
    path('subways/', Subways.as_view()),
    path('ip_data/', IpData.as_view()),
]