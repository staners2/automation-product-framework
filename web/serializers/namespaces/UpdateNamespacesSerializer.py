from django.utils import timezone
from rest_framework import serializers

from web.models.NamespacesModel import NamespacesModel


class UpdateNamespacesSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)

    class Meta:
        model = NamespacesModel
        exclude = ("updated", "deleted")

    def validate_title(self, value):
        if (
            NamespacesModel.objects.exclude(id=self.instance.id)
            .filter(
                title=self.initial_data.get("title", self.instance.title),
                deleted=None,
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError(
                "Пространство с таким названием уже существует!",
            )

        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.updated = timezone.now()
        instance.save()

        return instance
