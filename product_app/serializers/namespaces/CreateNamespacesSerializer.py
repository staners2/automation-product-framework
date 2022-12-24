from rest_framework import serializers

from product_app.models.NamespacesModel import NamespacesModel


class CreateNamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        fields = "__all__"

    # TODO: Валидацию на то что пространства уникальны
    def validate(self, attrs):
        if NamespacesModel.objects.filter(title=self.initial_data["title"]).count() != 0:
            raise serializers.ValidationError("Такое пространство уже существует!")

        return attrs

    def create(self, validated_data):
        title = validated_data.get("title")
        instance = NamespacesModel(
            title=title,
        )
        instance.save()

        return instance
