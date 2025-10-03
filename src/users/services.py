import uuid

from django.contrib.auth import get_user_model

from shared.cache import CacheService

from .models import ActivationKey
from .tasks import send_activation_mail, send_successful_activation_mail

User = get_user_model()

# func approach
# def create_activation_key(email: str) -> uuid.UUID:
#     return uuid.uuid3(namespace=uuid.uuid4(), name=email)  # for dynamic namespace
#     # return uuid.uuid3(namespace=USER_ACTIVATION_UUID_NAMESPACE, name=email) #for fixed namespace


# def create_activation_link(activation_key: uuid.UUID) -> str:
#     return f"https://frontend.com/users/activate/{activation_key}"


# def send_user_activation_email(email: str, activation_key: uuid.UUID) -> None:
#     """Send actiavtion email using SMTP."""

#     activation_link: str = create_activation_link(activation_key)

#     send_activation_mail.delay(recipient=email, activation_link=activation_link)


# class-based approach
class Activator:
    def __init__(self, email: str):
        self.email = email
        self.user = User.objects.get(email=email)

    def create_activation_key(self) -> uuid.UUID:
        return uuid.uuid3(namespace=uuid.uuid4(), name=self.email)

    def create_activation_link(self, activation_key: uuid.UUID) -> str:
        return f"https://frontend.com/users/activate/{activation_key}"

    def send_user_activation_email(self, activation_key: uuid.UUID) -> None:
        """Send actiavtion email using SMTP."""

        activation_link: str = self.create_activation_link(activation_key)

        send_activation_mail.delay(
            recipient=self.email, activation_link=activation_link
        )

    def save_activation_information(
        self, internal_user_id: int, activation_key: uuid.UUID
    ) -> None:
        # ActivationKey.objects.create(user=self.user, key=str(activation_key))
        cache = CacheService()
        payload = {"user_id": internal_user_id}
        cache.save(
            namespace="activation", key=activation_key, instance=payload, ttl=2000
        )

    def validate_activation_SQL(self, activation_key: uuid.UUID) -> None:
        """Validate the activation UUID in the cache.

        1. Buidl the key in the activation namespace:
            activation:fd531655-f638-456b-aabe-1c77482f379e
        2. Retrieve the record from the cache
        3. 404 if doesn't exist or the generation TTL is > 1day
        4. 200 if exists and update user.is_active to True
        """

        try:
            key = ActivationKey.objects.get(key=str(activation_key))
        except ActivationKey.DoesNotExist:
            raise ValueError("no such activation key in the DB")

        key.user.is_active = True
        key.user.save()
        key.delete()

        send_successful_activation_mail.delay(recipient=self.email)

        # create redis connection instance
        # generate the key based on the namespace
        # update the user.is_active to True

    @staticmethod
    def validate_activation_redis(activation_key: uuid.UUID):
        # connection = redis.Redis.from_url(settings.CACHE_URL, decode_responses=True)
        cache = CacheService()
        payload = cache.get(namespace="activation", key=activation_key)
        if not payload:
            raise ValueError("no such activation key in the cache")

        user_id = payload.get("user_id")
        cache.connection.delete(f"activation:{activation_key}")

        user = User.objects.get(id=user_id)
        if user.is_active:
            raise ValueError("user is already active")

        user.is_active = True
        user.save()
        send_successful_activation_mail.delay(recipient=user.email)  # type: ignore
