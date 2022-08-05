from rest_framework import serializers

from users.serializers import UserSerializer
from board.models import Ad, Category, Image, Tags, NecessaryField, FavoriteAd, FavoriteSeller
from locations.serializers import CountrySerializer, CitySerializer, AdressSerializer
from locations.models import Region, Adress
from datetime import datetime


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('source', )


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name')

class NecessaryFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = NecessaryField
        fields = ('name', 'type')


class CategorySerializer(serializers.ModelSerializer):
    parent = SubCategorySerializer()
    children = SubCategorySerializer(many=True)
    necessary_fields = NecessaryFieldSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'children', 'necessary_fields')


class UserAdSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = SubCategorySerializer()
    adress = AdressSerializer()
    tags = TagsSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Ad
        fields = fields = ('id', 'title', 'category', 'desc', 'price', 'date', 'tags', 'images')


class CreateAdSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField()
    region = serializers.IntegerField()
    street = serializers.CharField()
    house = serializers.CharField()
    data = serializers.JSONField()
    imgs = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Ad
        fields = (
            'price', 'title', 'category', 'desc', 'price', 'date', 'imgs', \
            'category', 'region', 'street', 'house', 'data', 'tags' \
        )

    def save(self, author):
        new_ad = Ad(
            price=self.validated_data['price'], title=self.validated_data['title'], \
            date=datetime.utcnow(), desc=self.validated_data['desc'], \
            category_id=self.validated_data['category'], author_id=author.id, \
            data=self.validated_data['data'], 
        )

        try:
            region = Region.objects.get(pk=self.validated_data['region'])
            new_adress = Adress(region=region, house=self.validated_data.get('house', None), \
                    street=self.validated_data.get('street', None) \
                )
            new_adress.save()
            new_ad.adress = new_adress
            new_ad.save()
            
            tags = [tag.id for tag in self.validated_data['tags']]
            new_ad.tags.set(tags)
            new_ad.save()

            for img in self.validated_data['imgs']:
                img = Image(source=img, ad=new_ad)
                img.save()

            return new_ad
        except Region.DoesNotExist: 
            raise serializers.ValidationError('Не удалось найти район с заданным id')

    def update(self, id):
        ad = Ad.objects.get(pk=id)

        try:
            if 'region' in self.validated_data:
                ad.adress.region = Region.objects.get(pk=self.validated_data['region'])
            if 'street' in self.validated_data:
                ad.adress.street = self.validated_data['street']
            if 'house' in self.validated_data:
                ad.adress.house = self.validated_data['house']
            if 'price' in self.validated_data:
                ad.price = self.validated_data['price']
            if 'title' in self.validated_data:
                ad.title = self.validated_data['title']
            if 'data' in self.validated_data:
                ad.data = self.validated_data['data']
            if 'desc' in self.validated_data:
                ad.desc = self.validated_data['desc']
            if 'category' in self.validated_data:
                ad.category_id = self.validated_data['category']

            ad.adress.save()
            ad.save()

            if 'imgs' in self.validated_data:
                for image in ad.images.all():
                    image.delete()

                for img in self.validated_data['imgs']:
                    img = Image(source=img, ad=ad)
                    img.save()

            return ad
        except Region.DoesNotExist: 
            raise serializers.ValidationError('Не удалось найти район с заданным id')


class SubAdSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Ad
        fields = ('id', 'title', 'price', 'tags', 'images')


class AdSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = CategorySerializer()
    adress = AdressSerializer()
    tags = TagsSerializer(many=True)
    images = ImageSerializer(many=True)
    
    class Meta:
        model = Ad
        fields = ('id', 'title', 'category', 'desc', 'price', 'date', 'author', 'adress', 'data', 'tags', 'images')


class CreateFavoriteAdsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteAd
        fields = ('id','favorite_ads',)

    def save(self, owner):
        favorite_ads = [favorite_ad.id for favorite_ad in self.validated_data['favorite_ads']]
        try:
            favorite_ads_qs = FavoriteAd.objects.get(owner=owner, favorite_ads__in=favorite_ads)
            favorite_ads_qs.delete()
            return f"Объявление/-я удалено/-ы из избранных"
        except FavoriteAd.DoesNotExist:
            new_favorite_ad = FavoriteAd.objects.create(owner=owner)
            new_favorite_ad.favorite_ads.set(favorite_ads)
            return f"Объявление/-я добавлено/-ы в избранное"

class FavoriteAdsSerializer(serializers.ModelSerializer):
    favorite_ads = AdSerializer(many=True)

    class Meta:
        model = FavoriteAd
        fields = ('id','favorite_ads',)

class CreateFavoriteSellersSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavoriteSeller
        fields = ('id','favorite_sellers',)

    def save(self, owner):
        favorite_sellers = [favorite_sellers.id for favorite_sellers in self.validated_data['favorite_sellers']]
        try:
            favorite_sellers_qs = FavoriteSeller.objects.get(owner=owner, favorite_sellers__in=favorite_sellers)
            favorite_sellers_qs.delete()
            return f"Продавец/-ы удалён/-ы из избранных"
        except FavoriteSeller.DoesNotExist:
            new_favorite_ad = FavoriteSeller.objects.create(owner=owner)
            new_favorite_ad.favorite_sellers.set(favorite_sellers)
            return f"Продавец/-ы добавлен/-ы в избранное"

class FavoriteSellersSerializer(serializers.ModelSerializer):
    favorite_sellers = UserSerializer(many=True)

    class Meta:
        model = FavoriteSeller
        fields = ('id','favorite_sellers',)