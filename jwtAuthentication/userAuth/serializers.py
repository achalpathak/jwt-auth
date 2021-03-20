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

    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    profile_photo = serializers.ImageField(required = False, allow_null=True)
    phone_number = serializers.CharField(max_length=10, required=True)
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(max_length=1, required=True)

    class Meta:
        model = userauth_models.User
        fields = ('email', 'password', 'first_name', 'last_name', 'profile_photo', 'phone_number', 'age', 'gender')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_profile_photo(self, image):
        # checks image size before saving
        MAX_FILE_SIZE = 1000000 # 1MB
        if image.size > MAX_FILE_SIZE:
            raise ValidationError("Profile photo size should be less than 1MB.")
        return image
    
    def validate_phone_number(self, phone):
        # checks if phone is already linked with a user
        if userauth_models.UserProfile.objects.filter(phone_number=phone).exists():
            raise ValidationError("Phone number is already linked with a user.")
        return phone

    def create(self, validated_data):
        fields = UserProfileSerializer.Meta().fields # fetched fields from profile serializer
        profile_data = {field: validated_data.pop(field) for field in fields if validated_data.get(field)}
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
                ['A user with this email and password is not found.']
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