from django.urls import path
from .views import *

urlpatterns=[
    #watchlist
    path('list/',WatchListAV.as_view(),name="movie-list"),
    path('<int:pk>/',WatchListDetailsAV.as_view(),name="movie-details"),

    #streamplatform
    path('stream/',StreamPlatformAV.as_view(),name="stream"),
    path('stream/<int:pk>/',StreamDetailsAV.as_view(),name="streamplatform-detail"),
]