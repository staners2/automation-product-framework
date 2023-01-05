from django.utils import timezone
from rest_framework import serializers

from web.models.EventTypesModel import EventTypesModel


class UpdateEventTypesSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)

    class Meta:
        model = EventTypesModel
        exclude = ("updated", "deleted")

    def validate_title(self, value):
        if (
            EventTypesModel.objects.exclude(id=self.instance.id)
            .filter(
                title=self.initial_data.get("title", self.instance.title),
                deleted=None,
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Тип события с таким названием уже существует!")

        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.point = validated_data.get("point", instance.point)
        instance.description = validated_data.get("description", instance.description)
        instance.updated = timezone.now()
        instance.save()

        return instance
