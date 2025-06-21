from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response

from .enums import Role

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "first_name", "last_name", "role")


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "role")

    def validate_role(self, value: str) -> str:
        if value not in Role.users():
            raise serializers.ValidationError(
                f"Invalid role: {value}. It has to be either: {Role.users()}"
            )
        return value

    def validate(self, attrs: dict) -> dict:
        attrs["password"] = make_password(attrs["password"])
        return attrs


class UserRegistrationPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "role")


class UserListCreateAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserRegistrationSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            UserRegistrationPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )

    def get(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserRetrieveDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = [
        "get",
        "put",
        "delete",
    ]
    serializer_class = UserSerializer
    lookup_url_kwarg = "id"

    # permission_classes = [
    #     permissions.IsAuthenticated, permissions.IsAdminUser
    # ]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def get_queryset(self):
        return User.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserRegistrationPublicSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data="user deleted", status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        serializer = UserRegistrationPublicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            UserRegistrationPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_200_OK,
        )


# def create_user(request: HttpRequest) -> JsonResponse:
#     if request.method != "POST":
#         raise NotImplementedError("Only POST method is allowed")

#     data: dict = json.loads(request.body)
#     user = User.objects.create_user(**data)
#     # user = User.objects.create(**data) # if you are using the User model instead of the UserManager

#     results = {
#         "id": user.id,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "role": user.role,
#         "is_active": user.is_active,
#     }

#     return JsonResponse(results)
