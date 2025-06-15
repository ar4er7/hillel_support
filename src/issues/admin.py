from django.contrib import admin

from .models import Issue, Message


class IssueInline(admin.StackedInline):
    model = Message
    extra = 0
    readonly_fields = ["timestamp"]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    inlines = [
        IssueInline,
    ]
    readonly_fields = [
        "title",
        "junior",
    ]

    list_display = [
        "id",
        "title",
        "junior",
        "senior",
        "status",
    ]

    ordering = [
        "id",
        "status",
        "junior",
    ]
