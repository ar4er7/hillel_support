from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from issues.api import IssuesAPI, IssuesRetrieveUpdateDeleteAPI
from users.api import UserCreateAPI, UserRetrieveUpdateAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", UserCreateAPI.as_view()),
    path("users/<int:id>", UserRetrieveUpdateAPI.as_view()),
    path("issues/", IssuesAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveUpdateDeleteAPI.as_view()),
    # Authentication
    path("auth/token/", TokenObtainPairView.as_view()),
]
