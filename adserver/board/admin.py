from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Ad, Category, Image, Tags, NecessaryField, FavoriteAd, FavoriteSeller


admin.site.register(Ad)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Image)
admin.site.register(Tags)
admin.site.register(NecessaryField)
admin.site.register(FavoriteAd)
admin.site.register(FavoriteSeller)