from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from config.old_code import get_current_market_state
from issues.api import IssuesAPI, IssuesRetrieveUpdateDeleteAPI
from users.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", create_user),
    path("issues/", IssuesAPI.as_view()),
    path("issues/<int:id>", IssuesRetrieveUpdateDeleteAPI.as_view()),
    # Authentication
    # path("auth/token/", token_obtain_pair),
    path("rate-check/", get_current_market_state),
    path("auth/token/", TokenObtainPairView.as_view()),
]
