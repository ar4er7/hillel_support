from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["user_permissions", "groups"]
    readonly_fields = [
        "password",
        "last_login",
        "date_joined",
        "is_superuser",
        "email",
    ]
