from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import uuid
from . import utils

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    class GenderChoices(models.TextChoices):
        CHOICE_MALE = 'M', 'Male'
        CHOICE_FEMALE = 'F', 'Female'
        CHOICE_OTHER = 'O', 'Other'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_photo = models.ImageField(upload_to=utils.user_profile_photo_path, null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True)
    age = models.PositiveIntegerField(null=False, blank=False)
    gender = models.CharField(max_length=1, choices=GenderChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "user_profile"