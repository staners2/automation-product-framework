from rest_framework import serializers

from product_app.models.EventTypesModel import EventTypesModel


class CreateEventTypesSerializer(serializers.ModelSerializer):

    description = serializers.CharField(required=False)

    class Meta:
        model = EventTypesModel
        fields = "__all__"

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        title = validated_data.get("title")
        point = validated_data.get("point")
        description = validated_data.get("product", None)
        instance = EventTypesModel(title=title, point=point, description=description)
        instance.save()

        return instance
