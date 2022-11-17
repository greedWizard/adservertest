from rest_framework import serializers

from locations.models import Country, State, City, Region, Adress, Subway, IP_City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = ('id', 'name', 'country')


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = City
        fields = ('id', 'name', 'state')


class RegionSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Region
        fields = ('id', 'name', 'city')

class SubwaySerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Subway
        fields = ('id', 'name', 'city')

class AdressSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    subway = SubwaySerializer(many=True)

    class Meta:
        model = Adress
        fields = ('id', 'region', 'street', 'house', 'subway')

class IPSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = IP_City
        fields = ('city',)