import uuid

from config import celery_app
from django.core.mail import send_mail


@celery_app.task
def send_activation_mail(recipient: str, activation_link: uuid.UUID):
    send_mail(
        subject="user activation",
        message=f"please activate your account: {activation_link}",
        from_email="admin@support.com",
        recipient_list=[recipient],
    )


@celery_app.task
def send_successful_activation_mail(recipient: str):
    send_mail(
        subject="Activation Successful",
        message="Your account has been successfully activated.",
        from_email="admin@support.com",
        recipient_list=[recipient],
    )
