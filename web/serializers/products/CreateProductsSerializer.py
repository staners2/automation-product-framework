from rest_framework import serializers

from web.models.ChatsModel import ChatsModel
from web.models.EmployeesModel import EmployeesModel
from web.models.NamespacesModel import NamespacesModel
from web.models.ProductsModel import ProductsModel


class CreateProductsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
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
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = ProductsModel
        exclude = ("updated", "deleted")

    def validate(self, attrs):
        if ProductsModel.objects.filter(title=attrs.get("title"), deleted=None).count() != 0:
            raise serializers.ValidationError("Продукт с таким названием уже существует!")

        return attrs

    def create(self, validated_data):
        title = validated_data.get("title")
        namespaces = validated_data.get("namespaces", [])
        chats = validated_data.get("chats", [])
        developers = validated_data.get("developers", [])
        manager = validated_data.get("manager", None)
        base_namespace = validated_data.get("base_namespace", None)
        base_chat_id = validated_data.get("base_chat_id", None)
        is_active = validated_data.get("is_active", True)
        instance = ProductsModel(
            title=title,
            base_namespace=base_namespace,
            base_chat_id=base_chat_id,
            manager=manager,
            is_active=is_active,
        )
        instance.save()
        instance.namespaces.add(*namespaces)
        instance.chats.add(*chats)
        instance.developers.add(*developers)
        instance.save()

        return instance
