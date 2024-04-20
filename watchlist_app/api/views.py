from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, generics,viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import *
from rest_framework import filters
from .serializers import *
from watchlist_app.models import *
from .permissions import *
from.throttling import *
from .pagination import *




# Modelviewset

"""class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
"""

# ReadOnlyModelViewSet
"""class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
"""
# class for stream platform using viewsets
class StreamPlatformVS(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def list(self,request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self,request,pk):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset,pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)

    def create(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def destroy(self,request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReviewCreate(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Watchlist.objects.get(pk=pk)


        # <--------------------------------------------------------------------------------->
        # check to the user is already reviewed or not
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie,review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        # <--------------------------------------------------------------------------------->




        # <--------------------------------------------------------------------------------->
        # review Rating and Rating count

        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']

        else:
            movie.avg_rating = (movie.avg_rating+serializer.validated_data['rating'])/2
        movie.number_rating=movie.number_rating+1
        movie.save()
        # <--------------------------------------------------------------------------------->

        serializer.save(watchlist=movie,review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()# if using this print all the reviews from the review model,instead create a function for queryset and specify the pk
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]# ReviewUserOrReadOnly is get from the permission class it checks the review owner
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'




# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView,mixins.UpdateModelMixin):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#


#views for streaming platform
class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True, context={'request': request})#the context is added from the HyperlinkRelatedfield
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class StreamDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,pk):
        try :
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error':'Platform Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform,context ={'request': request})
        return Response(serializer.data)

    def put(self,request,pk,):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




    def delete(self,request,pk):
        platform =StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    queryset = Watchlist.objects.all()# if using this print all the reviews from the review model,instead create a function for queryset and specify the pk
    serializer_class = WatchListSerializer
    # pagination_class = WatchlistPagination
    pagination_class = WatchlistLOPagination
    # permission_classes = [IsAuthenticated]

    # filtering
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title','platform__name']

    # searching
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title','=platform__name']# '=' is used here to use exact value the user search,if using ^ this symbol the user get first items starts with that he searches

    # Ordering
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['avg_rating']


    # combining filtering,searchin.ordering
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    filterset_fields = ['title','platform__name']
    search_fields = ['title','platform__name']
    ordering_fields = ['avg_rating']


# views for watchlist
class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request):
        movies = Watchlist.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)


    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)





class WatchListDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            return Response({'error':'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)


    def put(self,request,pk):
        movie = Watchlist.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk):
        movie = Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)

