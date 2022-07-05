from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.exceptions import PermissionDenied

from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from board.serializers import ( 
                                AdSerializer, CategorySerializer, 
                                UserAdSerializer, CreateAdSerializer, 
                            )
from board.models import Ad, Category

from rest_framework.permissions import IsAuthenticated


class UserAds(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404('Данного пользователя не существуе')

        ads = user.ads
        serializer = AdSerializer(ads, many=True)

        return Response({'info': serializer.data})


class Ads(APIView):
    def get(self, request):
        get_data = request.query_params

        ads = Ad.objects.all().order_by('-date')
        page = 1

        if 'category' in get_data:
            #ads = ads.filter(category__id=get_data['category'])
            categories = Category.objects.filter(id=get_data['category'])
            family_arr = []
            for category in categories:
                family_arr.append(category.id)
                for tree in category.get_descendants():
                    family_arr.append(tree.id)
            ads = ads.filter(category__id__in=family_arr).order_by('id')
        if 'page' in get_data:
            page = int(get_data['page'])
        if 'author' in get_data:
            ads = ads.filter(author__id=get_data['author'])
        if 'title' in get_data:
            ads = ads.filter(title__icontains=get_data['title'])
        if 'min_price' in get_data:
            ads = ads.filter(price__gte=get_data['min_price'])
        if 'max_price' in get_data:
            ads = ads.filter(price__lte=get_data['max_price'])
        if 'region' in get_data:
            regions = []
            try: 
                regions = [int(_) for _ in (get_data['region'].split(','))]
            except ValueError:
                pass

            ads = ads.filter(adress__region__id__in=regions)
        if 'city' in get_data:
            cities = []
            try: 
                cities = [int(_) for _ in (get_data['city'].split(','))]
            except ValueError:
                pass

            ads = ads.filter(adress__region__city__id__in=cities)
        if 'state' in get_data:
            states = []
            try: 
                states = [int(_) for _ in (get_data['state'].split(','))]
            except ValueError:
                pass

            ads = ads.filter(adress__region__city__state__id__in=states)

        paginator = Paginator(ads, 7)
        count = len(ads.all())
        ads = paginator.get_page(page)

        serializer = AdSerializer(ads.object_list, many=True)

        return Response({'count': count, 'info': serializer.data})

    def post(self, request):
        serializer = CreateAdSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            new_ad = serializer.save(request.user)
            return Response({'status': 'ok', 'created_ad': new_ad.id})
        return Response({'error': serializer.errors})


class AdView(APIView):
    def get(self, request, id: int):
        try:
            ad = Ad.objects.get(pk=id)
        except Ad.DoesNotExist:
            raise Http404('No ad found')
 
        serializer = AdSerializer(ad)
        return Response({'info': serializer.data})
    
    def delete(self, request, id, format=None):
        try:
            ad = Ad.objects.get(pk=id)
        except Ad.DoesNotExist:
            raise Http404('No ad found')

        if request.user.id != ad.author.id:
            return PermissionDenied()

        operation = ad.delete()

        if operation:
            return Response({'status': 'ok'})
        return Response({'status': 'error'})

    def patch(self, request, id, format=None):
        try:
            ad = Ad.objects.get(pk=id)
        except Ad.DoesNotExist:
            raise Http404('No ad found')

        if request.user.id != ad.author.id:
            return PermissionDenied()

        serializer = CreateAdSerializer(partial=True, data=request.data)

        if serializer.is_valid():
            updated = serializer.update(id)
            return Response({'status': 'ok', 'updated_ad': updated.id})


class Categories(APIView):
    def get(self, request):
        categories = Category.objects.all().order_by('name')
        categs = []

        for category in categories.all():
            if len(category.children.all()) > 0:
                categs.append(category)
                categs.extend(category.children.order_by('name').all())

        categories = categs
        serializer = CategorySerializer(categories, many=True)
        return Response({'info': serializer.data})


class CategoryAdsView(APIView):
    def get(self, request, id):
        category = Category.objects.get(pk=id)
        cat_serializer = CategorySerializer(category)

        return Response({'info': cat_serializer.data})