from django.urls import path
from rest_framework.authtoken.views import *


urlpatterns = [
    path('login/',obtain_auth_token,name="login"),
]