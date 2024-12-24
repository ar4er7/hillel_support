# from django.shortcuts import render

import json
import random
import string

from django.http import HttpRequest, JsonResponse

from issues.models import Issue


def get_issue(request) -> JsonResponse:
    # issues = Issue.objects.create()
    # issues = Issue.objects.update()
    # issues = Issue.objects.get()
    # issues = Issue.objects.delete()
    issues: list[Issue] = Issue.objects.all()

    results: list[dict] = [
        {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        }
        for issue in issues
    ]
    return JsonResponse(data={"results": results})


def random_str(length=10) -> str:
    return "".join([random.choice(string.ascii_letters) for i in range(length)])


def create_random_issue(request: HttpRequest) -> JsonResponse:
    issue: Issue = Issue.objects.create(
        title=random_str(length=20),
        body=random_str(length=30),
        senior_id=1,
        junior_id=2,
    )

    result = {
        "id": issue.id,
        "title": issue.title,
        "body": issue.body,
        "senior_id": issue.senior_id,
        "junior_id": issue.junior_id,
    }

    return JsonResponse(data=result)


def create_issue(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)

        title: str = data.get("title", random_str(length=10))
        body: str = data.get("body", random_str(length=25))
        senior_id = data.get("senior_id", 1)
        junior_id = data.get("junior_id", 2)

        issue: Issue = Issue.objects.create(
            title=title,
            body=body,
            senior_id=senior_id,
            junior_id=junior_id,
        )

        result = {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        }

    return JsonResponse(data=result)
