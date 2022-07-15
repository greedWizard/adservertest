from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Ad, Category, Image, NecessaryField


admin.site.register(Ad)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Image)
admin.site.register(NecessaryField)