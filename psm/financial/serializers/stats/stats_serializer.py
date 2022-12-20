from rest_framework.serializers import *


class StatsSerializer(Serializer):
    year = CharField()
    care_house = CharField()
    typology = CharField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
