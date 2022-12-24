from rest_framework import serializers

from product_app.models.ChatsModel import ChatsModel


class UpdateChatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatsModel
        fields = "__all__"

    # TODO: Валидацию на то что у одного продукта запись может быть только одна за месяц
    def validate(self, attrs):
        if ChatsModel.objects.exclude(id=self.instance.id).filter(title=self.initial_data["title"],
                                     chat_id=self.initial_data["chat_id"]).count() != 0:
            raise serializers.ValidationError("Такой чат уже существует!")

        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        instance.chat_id = validated_data.get("chat_id")
        instance.save()

        return instance
