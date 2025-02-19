from django.db import models

from users.models import User


class Issue(models.Model):
    title = models.CharField(max_length=100)
    status = models.PositiveBigIntegerField()

    junior = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="junior_issues"
    )
    senior = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="senior_issues"
    )
    body = models.TextField()

    def __repr__(self) -> str:
        return f"Issue[{self.pk} {self.title[:10]}]"


class Message(models.Model):
    body: str = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
