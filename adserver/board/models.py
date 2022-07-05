from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import JSONField, ArrayField
from rest_framework import serializers
from mptt.models import MPTTModel, TreeForeignKey
from locations.models import Adress

from board.validators import DataValidator


class NecessaryField(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=[
        ('number', 'число'),
        ('text', 'текст'),
    ])

    def __str__(self):
        return f'{self.name} {self.type}'


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = models.TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', \
        null=True, blank=True)
    necessary_fields = models.ManyToManyField(NecessaryField, related_name='categories', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=150, verbose_name='Title')
    desc = models.TextField(verbose_name='Description')
    price = models.IntegerField(validators=[MinValueValidator(0), ])
    date = models.DateTimeField(auto_now=True)

    adress = models.OneToOneField(Adress, on_delete=models.CASCADE, \
        related_name='ad')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ads')
    data = JSONField(default=dict)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        keys = self.data.keys()

        for field in self.category.necessary_fields.all():
            if not field.name in keys:
                raise serializers.ValidationError('Не все необходимые поля заданы')
        super(Ad, self).save(*args, **kwargs)


class Image(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    source = models.ImageField()

    def __str__(self):
        return f'{self.source}'

    def save(self, *args, **kwargs):
        ad = self.ad

        if len(Image.objects.filter(ad__id=ad.id).all()) > 10:
            raise serializers.ValidationError('Нельзя прикреплять больше 10 изображений к одному объявлению')
        super(Image, self).save(*args, **kwargs)