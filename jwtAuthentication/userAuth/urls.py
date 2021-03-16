
from django.urls import include, path

from . import apis


urlpatterns = [
    path('v1/signup', apis.UserRegistrationAPI.as_view()),
    path('v1/login', apis.UserLoginAPI.as_view()),
    
    #protected urls
    path('v1/profile', apis.UserProfileAPI.as_view()),
]