from rest_framework import serializers
from . import models as userauth_models
import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from datetime import datetime
from rest_framework.exceptions import ValidationError

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = userauth_models.UserProfile
        fields = ('first_name', 'last_name', 'profile_photo', 'phone_number', 'age', 'gender')
    
class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(required=True)

    class Meta:
        model = userauth_models.User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = userauth_models.User.objects.create_user(**validated_data)
        userauth_models.UserProfile.objects.create(
            user=user,
           **profile_data
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise ValidationError(
                'A user with this email and password is not found.'
            )
        payload = {
            'id': str(user.id),
            'email': user.email,
            'is_staff': user.is_staff,
            'token_expiry': str(datetime.now() + settings.JWT_CONFIGURATION['TOKEN_LIFETIME'])
        }
        jwt_token = jwt.encode(payload, settings.JWT_CONFIGURATION['SIGNING_KEY'], algorithm=settings.JWT_CONFIGURATION['ALGORITHM'])
        if settings.JWT_CONFIGURATION['UPDATE_LAST_LOGIN']:
            update_last_login(None, user)
        return {
            'email': user.email,
            'token': jwt_token
        }