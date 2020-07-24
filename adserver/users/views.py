from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissionsOrAnonReadOnly, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import Http404, HttpResponseForbidden

from users.serializers import  (
                            UserSerializer,
                            ProfileSerializer, 
                            CreateUserSerializer, 
                            ProfilePostSerializer, 
                            ProfileUpdateSerializer,
                            UserUpdateSerializer,
                        )
from users.models import Profile


class Users(APIView):
    def get(self, request):
        query_set = User.objects.all()
        serializer = UserSerializer(query_set, many=True)
        return Response({'info': serializer.data})


class CreateUser(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'ok', 'registred': user.email})

        return Response({'error': serializer.errors}, status=400)


class UpdateUserView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(request.user.id)
            return Response({'status': 'ok'})
        
        return Response({'error': serializer.errors}, status=401)


class AuthorizedUser(APIView):
    def get(self, request):
        try: 
            user = request.user
            serializer = UserSerializer(user)

            return Response({'info': serializer.data})
        except AttributeError:
            return Response({'error': 'Not logged in'}, status=400)


class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except:
            raise Http404('Not found')

        serializer = UserSerializer(user)

        return Response({'info': serializer.data})


class ProfileUpdateView(APIView):
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        profile = request.user.profile

        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})

        return Response({'error': serializer.errors}, status=400)
