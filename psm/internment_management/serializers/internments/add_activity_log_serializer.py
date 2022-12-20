from rest_framework.serializers import *


class AddActivityLogSerializer(Serializer):
    next_state = CharField()
    description = CharField()
    internment_id = CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass