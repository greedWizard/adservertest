from django.core.cache import cache
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.exceptions import PermissionDenied

from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from board.serializers import ( 
                                AdSerializer, CategorySerializer, 
                                UserAdSerializer, CreateAdSerializer, 
                            )
from board.models import Ad, Category
from board.filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
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

class SearchHistory(APIView):

    def get(self, request):
        search_history_cache_key = settings.SEARCH_HISTORY_TEMPLATE.format(user_id=request.user.id)
        search_history_cache = cache.get(search_history_cache_key)
        if search_history_cache is None:
            return Response({'error': 'Вы пока не сохранили ни одного поискового запроса'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'info': search_history_cache})

    def delete(self, request):
        try:
            search_history_cache_key = settings.SEARCH_HISTORY_TEMPLATE.format(user_id=request.user.id)
            cache.delete(search_history_cache_key)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Ошибка удаления'}, status=status.HTTP_400_BAD_REQUEST)  

class Ads(generics.ListCreateAPIView):
    queryset = Ad.objects.all().order_by('-date')
    serializer_class = AdSerializer
    pagination_class = PageNumberPagination
    page_size = 10
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        params = request.query_params.dict().copy()
        search_history_cache_key = settings.SEARCH_HISTORY_TEMPLATE.format(user_id=request.user.id)
        user_search_cache = cache.get(search_history_cache_key)
        if params != {}:
            if user_search_cache is None:
                cache.set(search_history_cache_key, [params], timeout=None)
            else:
                if params not in user_search_cache:
                    user_search_cache.insert(0, params)
                    cache.set(search_history_cache_key,  user_search_cache, timeout=None)

        queryset = self.filter_queryset(self.get_queryset())
               
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = AdSerializer(page, many=True)
            return self.get_paginated_response({'info': serializer.data})


        serializer = AdSerializer(queryset, many=True)
        return Response({'info': serializer.data})

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
        categories = Category.objects.filter(parent = None).order_by('name')
        categs = []

        for category in categories:
            categs.extend(category.get_descendants(include_self=True))

        categories = categs
        serializer = CategorySerializer(categories, many=True)
        return Response({'info': serializer.data})


class CategoryAdsView(APIView):
    def get(self, request, id):
        category = Category.objects.get(pk=id)
        cat_serializer = CategorySerializer(category)

        return Response({'info': cat_serializer.data})