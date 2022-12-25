from rest_framework import serializers

from product_app.models.ChatsModel import ChatsModel
from product_app.models.EmployeesModel import EmployeesModel
from product_app.models.EventsModel import EventsModel
from product_app.models.NamespacesModel import NamespacesModel
from product_app.models.ProductsModel import ProductsModel


class UpdateProductsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)
    namespaces = serializers.PrimaryKeyRelatedField(queryset=NamespacesModel.objects, required=False, many=True)
    chats = serializers.PrimaryKeyRelatedField(queryset=ChatsModel.objects, required=False, many=True)
    employees = serializers.PrimaryKeyRelatedField(queryset=EmployeesModel, required=False, many=True)

    base_namespace = serializers.PrimaryKeyRelatedField(queryset=NamespacesModel.objects, required=False, many=False)
    base_chat_id = serializers.PrimaryKeyRelatedField(queryset=ChatsModel.objects, required=False, many=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = ProductsModel
        fields = "__all__"

    def validate(self, attrs):
        if ProductsModel.objects.exclude(id=self.instance.id).filter(title=self.initial_data["title"]).count() != 0:
            raise serializers.ValidationError("Продукт с таким названием уже существует!")

        return attrs

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title")
        namespaces = validated_data.get("namespaces", instance.namespaces.all())
        chats = validated_data.get("chats", instance.chats.all())
        employees = validated_data.get("employees", instance.employees.all())
        instance.base_namespace = validated_data.get("base_namespace", instance.base_namespace)
        instance.base_chat_id = validated_data.get("base_chat_id", instance.base_chat_id)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.namespaces.add(*namespaces)
        instance.chats.add(*chats)
        instance.employees.add(*employees)
        instance.save()

        return instance
