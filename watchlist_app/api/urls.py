from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()
router.register('stream',StreamPlatformVS,basename='streamplatform')# also use in like cast and others

urlpatterns=[
    #watchlist
    path('list/',WatchListAV.as_view(),name="movie-list"),
    path('<int:pk>/',WatchListDetailsAV.as_view(),name="movie-details"),
    path('list2/',WatchList.as_view(),name="watch-list"),

    #streamplatform
    # path('stream/',StreamPlatformAV.as_view(),name="stream"),
    # path('stream/<int:pk>/',StreamDetailsAV.as_view(),name="streamplatform-detail"),
    path('',include(router.urls)),

    # path('stream/<int:pk>/review',StreamDetailsAV.as_view(),name="streamplatform-detail"),

    #review
    path('stream/movie/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('stream/movie/<int:pk>/reviews/',ReviewList.as_view(),name='review-list'),
    path('stream/review/<int:pk>/',ReviewDetail.as_view(),name='review-Detail'),
    path('reviews/',UserReview.as_view(),name='user-review-Detail'),
]