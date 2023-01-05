from django.utils import timezone
from rest_framework import serializers

from web.models.ChatsModel import ChatsModel
from web.models.EmployeesModel import EmployeesModel
from web.models.NamespacesModel import NamespacesModel
from web.models.ProductsModel import ProductsModel


class UpdateProductsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)
    namespaces = serializers.PrimaryKeyRelatedField(
        queryset=NamespacesModel.objects.filter(deleted=None).all(),
        required=False,
        many=True,
    )
    chats = serializers.PrimaryKeyRelatedField(
        queryset=ChatsModel.objects.filter(deleted=None).all(),
        required=False,
        many=True,
    )
    developers = serializers.PrimaryKeyRelatedField(
        queryset=EmployeesModel.objects.filter(deleted=None).all(),
        required=False,
        many=True,
    )
    manager = serializers.PrimaryKeyRelatedField(
        queryset=EmployeesModel.objects.filter(deleted=None).all(),
        required=False,
        many=False,
    )

    base_namespace = serializers.PrimaryKeyRelatedField(
        queryset=NamespacesModel.objects.filter(deleted=None).all(),
        required=False,
        many=False,
    )
    base_chat_id = serializers.PrimaryKeyRelatedField(
        queryset=ChatsModel.objects.filter(deleted=None).all(),
        required=False,
        many=False,
    )
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = ProductsModel
        exclude = ("updated", "deleted")

    def validate_title(self, value):
        if (
            ProductsModel.objects.exclude(id=self.instance.id)
            .filter(title=self.initial_data.get("title", self.instance.title), deleted=None)
            .count()
            != 0
        ):
            raise serializers.ValidationError("Продукт с таким названием уже существует!")

        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        namespaces = validated_data.get("namespaces", instance.namespaces.all())
        chats = validated_data.get("chats", instance.chats.all())
        developers = validated_data.get("developers", instance.developers.all())
        instance.manager = validated_data.get("manager", instance.manager)
        instance.base_namespace = validated_data.get("base_namespace", instance.base_namespace)
        instance.base_chat_id = validated_data.get("base_chat_id", instance.base_chat_id)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.namespaces.add(*namespaces)
        instance.chats.add(*chats)
        instance.developers.add(*developers)
        instance.updated = timezone.now()
        instance.save()

        return instance
