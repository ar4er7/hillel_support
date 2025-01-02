import json

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from issues.models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        # fields = ['id', 'title', 'body', 'junior_id']
        fields = "__all__"
        # exclude = ['id',]


@api_view(
    [
        "GET",
    ]
)
def get_issue(request) -> Response:
    issues: list[Issue] = Issue.objects.all()
    results: list[IssueSerializer] = [IssueSerializer(issue).data for issue in issues]

    return Response(data={"results": results})


@api_view(
    [
        "GET",
    ]
)
def retrieve_issue(request, issue_id: int) -> Response:
    instance = get_object_or_404(Issue, id=issue_id)
    # try:
    #     instance:Issue = Issue.objects.get(id=issue_id)
    # except Issue.DoesNotExist:
    #     raise Http404

    return Response(data=IssueSerializer(instance).data)


@api_view(["POST"])
def create_issue(request) -> Response:
    try:
        payload: dict = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        raise Exception("Request body is invalid")

    serializer = IssueSerializer(data=payload)
    serializer.is_valid(raise_exception=True)

    issue = Issue.objects.create(**serializer.validated_data)
    # issue = Issue.objects.create(
    #     title = serializer.validated_data['title'],
    #     body = serializer.validated_data['body'],
    #     junior_id = serializer.validated_data['junior_id'],
    #     senior_id = serializer.validated_data['senior_id'],
    # )

    return Response(data=IssueSerializer(issue).data)
