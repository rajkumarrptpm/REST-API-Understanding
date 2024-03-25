from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from watchlist_app.models import *


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

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Watchlist.objects.get(pk=pk)
        serializer.save(watchlist=movie)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()# if using this print all the reviews from the review model,instead create a function for queryset and specify the pk
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist = pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all
    serializer_class = ReviewSerializer





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

# views for watchlist
class WatchListAV(APIView):

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
