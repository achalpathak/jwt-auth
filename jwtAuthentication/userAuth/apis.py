from rest_framework import status
from . import models as userauth_models
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from . import serializers
from . import permissions as custom_permissions

class UserRegistrationAPI(CreateAPIView):

    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('User registered successfully', status=status.HTTP_201_CREATED)

class UserLoginAPI(RetrieveAPIView):

    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

class UserProfileAPI(RetrieveAPIView):

    permission_classes = [custom_permissions.IsTokenVerified]
    serializer_class = serializers.UserProfileSerializer

    def get(self, request):
        profile_obj = userauth_models.UserProfile.objects.get(user_id=request.user_details['id'])
        serializer = self.serializer_class(profile_obj)
        return Response(serializer.data)