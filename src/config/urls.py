from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from config.old_code import get_current_market_state
from issues.api import create_issue, get_issue, retrieve_issue

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issue),
    path("issues/<int:issue_id>", retrieve_issue),
    path("issues/create/", create_issue),
    path("rate-check/", get_current_market_state),
    # Authentication
    # path("auth/token/", token_obtain_pair),
    path("auth/token/", TokenObtainPairView.as_view()),
]
