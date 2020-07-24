from django.urls import path, include
from locations.views import Countries, Cities, States, Regions

urlpatterns = [
    path('countries/', Countries.as_view()),
    path('states/', States.as_view()),
    path('cities/', Cities.as_view()),
    path('regions/', Regions.as_view()),
]