from django.utils import timezone
from rest_framework import serializers

from product_app.models.ChatsModel import ChatsModel


class UpdateChatsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)
    chat_id = serializers.CharField(required=False)

    class Meta:
        model = ChatsModel
        exclude = ("updated", "deleted")

    # TODO: Валидацию на то что у одного продукта запись может быть только одна за месяц
    def validate(self, attrs):
        if (
            ChatsModel.objects.exclude(id=self.instance.id)
            .filter(
                title=attrs.get("title", self.instance.title),
                chat_id=attrs.get("chat_id", self.instance.chat_id),
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Такой чат уже существует!")

        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", self.instance.title)
        instance.chat_id = validated_data.get("chat_id", self.instance.chat_id)
        instance.updated = timezone.now()
        instance.save()

        return instance
