from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')# also use in like cast and others

urlpatterns=[
    #watchlist
    path('list/',WatchListAV.as_view(),name="movie-list"),
    path('<int:pk>/',WatchListDetailsAV.as_view(),name="movie-details"),

    #streamplatform
    # path('stream/',StreamPlatformAV.as_view(),name="stream"),
    # path('stream/<int:pk>/',StreamDetailsAV.as_view(),name="streamplatform-detail"),
    path('',include(router.urls)),

    # path('stream/<int:pk>/review',StreamDetailsAV.as_view(),name="streamplatform-detail"),

    #review
    path('stream/movie/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/reviews/',ReviewList.as_view(),name='review-list'),
    path('stream/reviews/<int:pk>',ReviewDetail.as_view(),name='review-Detail'),
]