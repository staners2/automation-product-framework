from rest_framework import serializers

from product_app.models.EventTypesModel import EventTypesModel
from product_app.models.EventsModel import EventsModel


class UpdateEventTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTypesModel
        fields = "__all__"

    def validate(self, attrs):
        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.point = validated_data.get("point", instance.point)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        return instance
