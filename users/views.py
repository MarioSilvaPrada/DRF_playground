from users.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, status
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


from users.models import CustomUser

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            print('account', account)

            token = Token.objects.get(user=account).key

            print('token', token)
       

            data['user']= serializer.data
            data['token'] = token
        return Response(data, status=status.HTTP_201_CREATED)
        # return self.create(request, *args, **kwargs)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data = {}
        data['name'] = user.name
        data['email'] = user.email
        
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'user': data}, status=status.HTTP_200_OK)
