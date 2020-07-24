from django.contrib import admin

from locations.models import Country, City, Adress, State, Region


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Adress)
admin.site.register(Region)
admin.site.register(State)