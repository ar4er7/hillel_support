from django.contrib import admin
from django.urls import path

from issues.api import create_issue, get_issue, retrieve_issue

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issue),
    path("issues/<int:issue_id>", retrieve_issue),
    path("issues/create/", create_issue),
]
