from rest_framework import serializers

from web.models.NamespacesModel import NamespacesModel


class CreateNamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        exclude = ("updated", "deleted")

    def validate_title(self, value):
        if (
            NamespacesModel.objects.filter(
                title=value,
                deleted=None,
            ).count()
            != 0
        ):
            raise serializers.ValidationError(
                "Пространство с таким названием уже существует!",
            )
        return value

    def create(self, validated_data):
        title = validated_data.get("title")
        instance = NamespacesModel(
            title=title,
        )
        instance.save()

        return instance
