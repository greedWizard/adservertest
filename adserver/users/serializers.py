from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from users.models import Profile
from board.models import Ad, Category


class CreateUserSerializer(serializers.ModelSerializer):
    first_name =   serializers.CharField(required=True)
    last_name =     serializers.CharField(required=True)
    phone_number =  serializers.CharField(required=True)
    password2 =     serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'password2')

    def save(self):
        user =  User(
                    email=self.validated_data['email'],
                    username=self.validated_data['username'],
                )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'пароли должны совпадать'})

        user.set_password(password)
        user.save()
        
        profile = Profile(
                        first_name = self.validated_data['first_name'],
                        last_name = self.validated_data['last_name'],
                        phone_number = self.validated_data['phone_number'],
                        user=user,
                    )
        profile.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'new_password', 'new_password2', 'password', 'password2')

    
    def save(self, user_id):
        data = {}
        
        user = User.objects.get(pk=user_id)

        if not user.check_password(self.validated_data['password']):
            raise serializers.ValidationError({'password': 'Неверный пароль'})

        success = True

        if self.validated_data['password'] != self.validated_data['password2']:
            self.validated_data['password'] = 'Пароли не совпадают'
            success = False
        
        if 'new_password' in self.validated_data:
            if self.validated_data['new_password'] != self.validated_data['new_password2']:
                data['new_password'] = 'Новые пароли не совпадают'
                success = False
        
        if not user.check_password(self.validated_data['password']):
            data['password'] = 'Неверный пароль'
            success = False
        
        if success:
            if 'new_password' in self.validated_data:
                user.set_password(self.validated_data['new_password'])

            if 'username' in self.validated_data:
                user.username = self.validated_data['username']
            
            if 'email' in self.validated_data:
                user.email = self.validated_data['email']
            user.save()
            
            return user
        return None



class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'profile_pic')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'profile_pic')


class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_number', 'profile_pic')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'last_login', 'date_joined', 'profile')