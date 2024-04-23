from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .api import serializers
from watchlist_app import models

# Create your tests here.
class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testcase",password="NewPassword@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 streaming platform",website="http://www.netflix.com")

    def test_streamplatform_create(self):
        data={
            "name": "Netflix",
            "about": "#1 streaming platform",
            "website": "http://www.netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_steamingplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamplatform_put(self):
        data={
            "name": "Netflix2",
            "about": "#1 streaming platform updated",
            "website": "http://www.netflixupdated.com"
        }
        response = self.client.put(reverse('streamplatform-detail',args=(self.stream.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    def test_streamplatform_delete(self):
        response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WacthlistTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testcase",password="NewPassword@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",about="#1 streaming platform",website="http://www.netflix.com")
        self.watchlist = models.Watchlist.objects.create(platform=self.stream,title="John wick",description="action",active=True)
    def test_watchlist_create(self):
        data={
            "platform": self.stream,
            "title": "John wick",
            "description": "action thriller",
            "active": True
        }
        response = self.client.post(reverse('movie-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.Watchlist.objects.count(),1)
        self.assertEqual(models.Watchlist.objects.get().title,'John wick')


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testcase", password="NewPassword@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix", about="#1 streaming platform",
                                                           website="http://www.netflix.com")
        self.watchlist = models.Watchlist.objects.create(platform=self.stream, title="John wick", description="action",
                                                         active=True)
        self.watchlist2 = models.Watchlist.objects.create(platform=self.stream, title="Dark", description="sci-fi",
                                                         active=True)
        self.review = models.Review.objects.create(review_user=self.user,rating=4,description="good series",
                                                   watchlist=self.watchlist2,active=False)
    def test_review_create(self):
        data={
            "review_user": self.user,
            "rating": 4,
            "description": "good movie",
            "watchlist": self.watchlist,
            "active": True
        }
        response = self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(),2)
        # self.assertEqual(models.Review.objects.get().rating,4)


        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_review_create_unauth(self):

        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "good movie",
            "watchlist": self.watchlist,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_review_update(self):

        data={
            'review_user': self.user,
            'rating': 5,
            'description': 'good movie updated',
            'watchlist': self.watchlist,
            'active': False
        }

        response = self.client.put(reverse('review-Detail', args=(self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('review-list',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review-Detail',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse('review-Detail',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/api/watchlist/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)






