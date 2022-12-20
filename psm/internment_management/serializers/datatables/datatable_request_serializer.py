from rest_framework.serializers import *


class DataTableRequestSerializer(Serializer):
    draw = IntegerField()
    order_column = CharField()
    order_direction = CharField()
    start = IntegerField()
    length = IntegerField()
    search = CharField(allow_null=True, allow_blank=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass