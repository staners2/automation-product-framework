from rest_framework import serializers

from product_app.models.NamespacesModel import NamespacesModel


class UpdateNamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        fields = "__all__"

    # TODO: Валидацию на то что пространства уникальны
    def validate(self, attrs):
        if (
            NamespacesModel.objects.exclude(id=self.instance.id)
            .filter(
                title=self.initial_data["title"],
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Такое пространство уже существует!")

        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.chat_id = validated_data.get("chat_id")
        instance.save()

        return instance
