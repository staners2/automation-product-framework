from rest_framework import serializers

from web.models.EventTypesModel import EventTypesModel


class CreateEventTypesSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False)

    class Meta:
        model = EventTypesModel
        exclude = ("updated", "deleted")

    def validate_title(self, value):
        if (
            EventTypesModel.objects.filter(
                title=value,
                deleted=None,
            ).count()
            != 0
        ):
            raise serializers.ValidationError("Тип события с таким названием уже существует!")

        return value

    def create(self, validated_data):
        title = validated_data.get("title")
        point = validated_data.get("point")
        description = validated_data.get("product", None)
        instance = EventTypesModel(title=title, point=point, description=description)
        instance.save()

        return instance
