from rest_framework.serializers import *


class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField()
    remember_user = BooleanField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
