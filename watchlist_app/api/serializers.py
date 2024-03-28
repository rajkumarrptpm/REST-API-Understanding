from rest_framework import serializers
from watchlist_app.models import *



class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    # len_name = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True,read_only="True")
    class Meta:
        model = Watchlist
        fields = "__all__"
        # exclude =['active']
        # fields = ['name','description','active']

class StreamPlatformSerializer(serializers.ModelSerializer):
# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):

    # ------------
    # nested serializer
    watchlist = WatchListSerializer(many=True,read_only=True)# one streaming platform can have many movies
    # ----------

    # ------------
    # primary key of items in serializer
    # watchlist = serializers.PrimaryKeyRelatedField(many=True,read_only=True)# one streaming platform can have many movies
    # ----------

    # ------------
    # primary key of items in serializer
    # watchlist = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="movie-details")  # one streaming platform can have many movies

    # ----------


    class Meta:
        model = StreamPlatform
        fields = "__all__"

    """def get_len_name(self,object):
        length = len(object.name)
        return length

    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and description should be different")
        else:
            return data

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Name is too short!")
        else:
            return value"""
