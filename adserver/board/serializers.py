from rest_framework import serializers

from users.serializers import UserSerializer
from board.models import Ad, Category, Image, NecessaryField
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
    images = ImageSerializer(many=True)

    class Meta:
        model = Ad
        fields = fields = ('id', 'title', 'category', 'desc', 'price', 'date', 'images')


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
            'category', 'region', 'street', 'house', 'data', \
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
    images = ImageSerializer(many=True)

    class Meta:
        model = Ad
        fields = ('id', 'title', 'price', 'images')


class AdSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = CategorySerializer()
    adress = AdressSerializer()
    images = ImageSerializer(many=True)
    
    class Meta:
        model = Ad
        fields = ('id', 'title', 'category', 'desc', 'price', 'date', 'author', 'adress', 'data', 'images')