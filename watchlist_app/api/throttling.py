from rest_framework.throttling import *


class ReviewCreateThrottle(UserRateThrottle):
    scope = "review-create"


class ReviewListThrottle(UserRateThrottle):
    scope = "review-list"
