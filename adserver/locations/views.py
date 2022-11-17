from ipaddress import ip_address
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translate import Translator
from locations.models import Country, State, City, Region, Subway, IP_City
from locations.serializers import CountrySerializer, StateSerializer, CitySerializer, RegionSerializer, SubwaySerializer, IPSerializer


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

class Subways(APIView):
    def get(self, request):
        get_data = request.query_params

        subways = Subway.objects.filter(city_id=get_data['city_id'])

        try:
            subways  = subways.filter(name=get_data['name'])
        except:
            pass

        serializer = SubwaySerializer(subways, many=True)

        return Response({'info': serializer.data})


class IpData(APIView):
    def get(self, request):
        get_data = request.query_params
        city_ru = Translator(to_lang="ru").translate(get_data['city'])
        try:
            city = City.objects.get(name=city_ru)
            serializer = CitySerializer(city)
            return Response({'info': serializer.data})
        except City.DoesNotExist:
            return Response({'error': 'Не удалось определить город автоматически!'}, status=status.HTTP_400_BAD_REQUEST)