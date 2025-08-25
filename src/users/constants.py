import uuid

USER_ACTIVATION_UUID_NAMESPACE = uuid.uuid3(
    namespace=uuid.NAMESPACE_DNS, name="activation"
)
