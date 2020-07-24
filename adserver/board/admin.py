from django.contrib import admin

from .models import Ad, Category, Image, NecessaryField


admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(NecessaryField)