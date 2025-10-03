import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from . import services
from .enums import Role
from .models import ActivationKey

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


class UserActivationSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    key = serializers.UUIDField(write_only=True)

    class Meta:
        model = ActivationKey
        fields = ("key", "user_email")


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

        # # functional approach
        # activation_key: uuid.UUID = services.create_activation_key(
        #     email=serializer.data["email"]
        # )
        # services.send_user_activation_email(
        #     email=serializer.data["email"], activation_key=activation_key
        # )

        # OOP approach
        activation_service = services.Activator(email=serializer.data["email"])
        activation_key: uuid.UUID = activation_service.create_activation_key()

        activation_service.save_activation_information(
            internal_user_id=serializer.instance.id,
            activation_key=activation_key,
        )

        activation_service.send_user_activation_email(activation_key=activation_key)

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


@api_view(["POST"])
def resend_activation_mail(request):  # -> Response:
    breakpoint()
    pass


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def activate_user(request) -> Response:
    serializer = UserActivationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    """assuring Pylance that "is_valid" is a dict and has keys and values"""
    if not isinstance(serializer.validated_data, dict):
        raise TypeError("validated_data is not a dict")

    recieved_key = serializer.validated_data["key"]

    # try:
    #     activation_key = ActivationKey.objects.get(
    #         key=recieved_key
    #     )  # try to get the activation key from the DB
    # except ActivationKey.DoesNotExist:
    #     return Response(
    #         {"no such activation key in the DB"}, status=status.HTTP_404_NOT_FOUND
    #     )

    # email: str = activation_key.user.email
    # # get the email from the user associated with the activation key

    # activation_service = services.Activator(email=email)
    # # create an instance of the Activator service class

    try:
        # activation_service.validate_activation_SQL(activation_key=(recieved_key))
        services.Activator.validate_activation_redis(activation_key=(recieved_key))
    except ValueError:
        return Response({"wrong_activation_key"}, status=status.HTTP_404_NOT_FOUND)

    return Response(
        {"message": "User activated successfully"}, status=status.HTTP_200_OK
    )


class UserRetrieveDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = [
        "get",
        "put",
        "delete",
    ]
    serializer_class = UserSerializer
    lookup_url_kwarg = "id"

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
