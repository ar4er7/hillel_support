from django.db.models import Q
from rest_framework import generics, permissions, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.enums import Role

from .enums import Status
from .models import Issue


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

    def validate(self, attrs):
        attrs["status"] = Status.OPENED
        return attrs


class IssuesAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def post(self, request):
        if request.user.role != Role.JUNIOR:
            raise Exception("only juniors can create issues")

        return self.create(request)

    def get(self, request):
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
