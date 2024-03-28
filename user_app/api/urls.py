from django.urls import path
from rest_framework.authtoken.views import *
from .views import *

urlpatterns = [
    path('login/', obtain_auth_token, name="login"),
    path('register/', Registration.as_view(), name="register"),
    path('logout/', Logout.as_view(), name="logout"),
]