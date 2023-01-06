from django.utils import timezone
from rest_framework import serializers

from web.models.ChatsModel import ChatsModel


class UpdateChatsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)
    chat_id = serializers.CharField(required=False)

    class Meta:
        model = ChatsModel
        exclude = ("updated", "deleted")

    # TODO: Валидацию на то что у одного продукта запись может быть только одна за месяц
    def validate_title(self, value):
        if (
            ChatsModel.objects.exclude(id=self.instance.id)
            .filter(
                title=self.initial_data.get(
                    "title",
                    self.instance.title,
                ),
                deleted=None,
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Чат с таким названием уже существует!")

        return value

    def validate_chat_id(self, value):
        if (
            ChatsModel.objects.exclude(id=self.instance.id)
            .filter(
                deleted=None,
                chat_id=self.initial_data.get("chat_id", self.instance.chat_id),
            )
            .count()
            != 0
        ):
            raise serializers.ValidationError("Чат с таким ID уже существует!")

        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", self.instance.title)
        instance.chat_id = validated_data.get("chat_id", self.instance.chat_id)
        instance.updated = timezone.now()
        instance.save()

        return instance
