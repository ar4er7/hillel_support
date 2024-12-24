from django.contrib import admin
from django.urls import path

from issues.api import create_issue, create_random_issue, get_issue

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issue),
    path("issues/create/", create_issue),
    path("issues/create-random/", create_random_issue),
]
