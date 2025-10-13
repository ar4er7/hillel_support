from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response

from users.enums import Role

from .enums import Status
from .models import Issue, Message


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" and request.user.role != Role.ADMIN:
            raise PermissionDenied("Only admins can delete issues")

        if request.method == "PUT" and request.user.role not in [
            Role.SENIOR,
            Role.ADMIN,
        ]:
            raise PermissionDenied("Only seniors and admins can update issues")

        if request.method in ["GET", "PATCH"] and request.user.role not in [
            Role.JUNIOR,
            Role.SENIOR,
            Role.ADMIN,
        ]:
            raise PermissionDenied(
                "Only juniors, seniors, and admins can view or partially update issues"
            )
        return True


class IssueSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)
    junior = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Issue
        fields = "__all__"

    def create(self, validated_data):
        validated_data["status"] = Status.OPENED
        return super().create(validated_data)


class IssuesAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def post(self, request):
        """Create an issue. You must be authorized via Role.JUNIOR to create an issue.
        The issue will be set to OPENED and automatically assigned to the junior creating it.
        """
        if request.user.role != Role.JUNIOR:
            raise Exception("only juniors can create issues")
        return self.create(request)

    def get(self, request):
        """Get list of all the issues from the database"""
        queryset = self.get_queryset()
        if request.user.role == Role.SENIOR:
            queryset = queryset.filter(Q(senior=request.user) | Q(senior=None))
        elif request.user.role == Role.JUNIOR:
            queryset = queryset.filter(junior=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IssuesRetrieveUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "put", "patch", "delete"]
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()
    permission_classes = [RolePermission]
    lookup_url_kwarg = "id"

    def get(self, *args, **kwargs):
        """Get an exact issue by its id from the database. ALL AUTHORIZED ROLES"""
        return super().get(self, *args, **kwargs)

    def put(self, *args, **kwargs):
        """Update an issue completely. All fields must be provided.SENIORS and ADMINS only"""
        return super().put(self, *args, **kwargs)

    def patch(self, *args, **kwargs):
        """Update an issue partially with provided fields. ALL AUTHORIZED ROLES"""
        return super().patch(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete an issue by its id from the database. ADMINS only"""
        return super().delete(self, *args, **kwargs)


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())

    class Meta:
        model = Message
        fields = ["id", "body", "timestamp", "issue", "user"]

    def save(self):
        if user := self.validated_data.pop("user", None):  # type: ignore
            self.validated_data["user_id"] = user.id  # type: ignore
        if (issue := self.validated_data.pop("issue", None)) is not None:  # type: ignore
            self.validated_data["issue_id"] = issue.id  # type: ignore
        return super().save()


@swagger_auto_schema(
    method="get",
    operation_description="Get all messages for an issue with given id",
    responses={200: MessageSerializer(many=True)},
)
@swagger_auto_schema(
    method="post",
    operation_description="create a message for an issue with given id",
    request_body=MessageSerializer,
)
@api_view(["GET", "POST"])
def messages_api_dispatcher(request: Request, issue_id):
    if request.method == "GET":
        messages = Message.objects.filter(
            Q(issue__id=issue_id)
            & (
                Q(
                    issue__senior=request.user,
                )
                | Q(
                    issue__junior=request.user,
                )
            )
        ).order_by("-timestamp")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        issue = Issue.objects.get(id=issue_id)
        payload = request.data | {"issue": issue.id}  # type: ignore
        serializer = MessageSerializer(data=payload, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def issues_close(request: Request, id: int):
    """Setting the issue's stat to CLOSED. Only SENIOR"""
    issue = Issue.objects.get(id=id)

    if request.user.role != Role.SENIOR:
        raise PermissionDenied("Only the senior can close issues")

    if issue.status != Status.IN_PROGRESS or issue.senior is None:
        return Response(
            {"detail": "Issue is not in progress or not taken by a senior"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    issue.status = Status.CLOSED
    issue.save()
    serializer = IssueSerializer(issue)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def issues_take(request: Request, id: int):
    """Assinging an authorized Senior to an Issue and setting its stat to IN_PROGRESS"""
    issue = Issue.objects.get(id=id)

    if request.user.role != Role.SENIOR:
        raise PermissionDenied("Only the senior can take issues")

    if issue.status != Status.OPENED or issue.senior is not None:
        return Response(
            {"detail": "Issue is not opened or already taken"},
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    else:
        issue.status = Status.IN_PROGRESS
        issue.senior = request.user
        issue.save()
        serializer = IssueSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)
