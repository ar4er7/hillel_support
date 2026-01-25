from django.db import models

# from shared.django import TimestampMixin #If you need timestamp field
from users.models import User

from .enums import Status


class Issue(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(null=True)
    status = models.PositiveBigIntegerField(
        choices=Status.choices(), default=Status.OPENED
    )

    junior = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="junior_issues",
    )
    senior = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="senior_issues",
        blank=True,
    )

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"

    def __str__(self) -> str:
        return f"{self.title[:10]}"


class Message(models.Model):
    # class Meta:
    #     db_table = "messages"
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
