from users.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, status
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from users.models import CustomUser

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        account = serializer.save()
        token, created = Token.objects.get_or_create(user=account)
        
        headers = self.get_success_headers(serializer.data)
        return Response({'data':serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)

 


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
