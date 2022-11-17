from django.contrib import admin

from locations.models import Country, City, Adress, State, Region, IP_City, Subway


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Adress)
admin.site.register(Region)
admin.site.register(Subway)
admin.site.register(State)
admin.site.register(IP_City)