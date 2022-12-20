from rest_framework.serializers import *


class DailyValueSerializer(Serializer):
    value = FloatField()
    start_date = DateField(input_formats=['%d/%m/%Y'])

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
