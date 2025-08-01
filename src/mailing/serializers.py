from rest_framework import serializers


class Message(serializers.Serializer):
    sender = serializers.EmailField()
    recipient = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    body = serializers.CharField()
