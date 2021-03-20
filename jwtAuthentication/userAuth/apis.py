from rest_framework import status
from . import models as userauth_models
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from . import serializers
from . import permissions as custom_permissions

class UserRegistrationAPI(CreateAPIView):
    """
    User SignUp view
    """

    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('User registered successfully', status=status.HTTP_201_CREATED)

class UserLoginAPI(CreateAPIView):
    """
    User Login view
    """

    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'token' : serializer.data['token'],
            }
        return Response(response)

class UserProfileAPI(RetrieveAPIView):
    """
    User Profile view (protected view can only be accesed by authenticated user)
    """
    permission_classes = [custom_permissions.IsTokenVerified]
    serializer_class = serializers.UserProfileSerializer

    def get(self, request):
        profile_obj = userauth_models.UserProfile.objects.get(user_id=request.user_details['id'])
        serializer = self.serializer_class(profile_obj)
        return Response(serializer.data)