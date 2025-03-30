from rest_framework import generics, serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )  ## to ensure password is not returned in the response

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "role"]

    def create(self, data):
        user = User.objects.create_user(**data)
        return user


class UserAPI(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = UserSerializer

    def post(self, request):
        return self.create(request)


class UserRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    http_method_names = ["get", "put"]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id"


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
