from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from locations.models import Country, State, City, Region
from locations.serializers import CountrySerializer, StateSerializer, CitySerializer, RegionSerializer


class Countries(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)

        return Response({'info': serializer.data})


class States(APIView):
    def get(self, request):
        get_data = request.query_params

        states = State.objects.filter(country_id=get_data['country_id'])

        try:
            states = states.filter(name=get_data['name'])
        except:
            pass

        serializer = StateSerializer(states, many=True)

        return Response({'info': serializer.data})


class Cities(APIView):
    def get(self, request):
        get_data = request.query_params

        cities = City.objects.filter(state_id=get_data['state_id'])

        if 'name' in get_data:
            cities = cities.filter(name=get_data['name'])

        serializer = CitySerializer(cities, many=True)

        return Response({'info': serializer.data})


class Regions(APIView):
    def get(self, request):
        get_data = request.query_params

        regions = Region.objects.filter(city_id=get_data['city_id'])

        try:
            regions = regions.filter(name=get_data['name'])
        except:
            pass

        serializer = RegionSerializer(regions, many=True)

        return Response({'info': serializer.data})