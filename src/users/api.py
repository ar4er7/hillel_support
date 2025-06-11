from django.contrib.auth import get_user_model, hashers
from rest_framework import generics, serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(
    #     write_only=True
    # )  ## to ensure password is not returned in the response

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "password"]

    def create(self, data):
        user = User.objects.create_user(**data)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None) 
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserCreateAPI(generics.CreateAPIView):
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
