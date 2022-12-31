from rest_framework import serializers

from web.models.NamespacesModel import NamespacesModel


class CreateNamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        exclude = ("updated", "deleted")

    def validate(self, attrs):
        if NamespacesModel.objects.filter(title=self.initial_data["title"], deleted=None).count() != 0:
            raise serializers.ValidationError("Такое пространство уже существует!")

        return attrs

    def create(self, validated_data):
        title = validated_data.get("title")
        instance = NamespacesModel(
            title=title,
        )
        instance.save()

        return instance
