from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class State(models.Model):
    name = models.CharField(max_length=200, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return f'{self.name}'


class City(models.Model):
    name = models.CharField(max_length=200, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class Region(models.Model):
    name = models.CharField(max_length=200, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f'{self.city.name}, {self.name}'


class Adress(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='adresses')
    street = models.CharField(max_length=200, blank=True, null=True)
    house = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.street}, {self.house}'