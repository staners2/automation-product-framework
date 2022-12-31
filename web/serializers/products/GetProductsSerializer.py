from rest_framework import serializers

from web.models.ProductsModel import ProductsModel
from web.serializers.chats.GetChatsSerializer import GetChatsSerializer
from web.serializers.employees.GetEmployeesSerializer import GetEmployeesSerializer
from web.serializers.namespaces.GetNamespacesSerializer import GetNamespacesSerializer


class GetProductsSerializer(serializers.ModelSerializer):

    namespaces = GetNamespacesSerializer(many=True, required=False)
    chats = GetChatsSerializer(many=True, required=False)
    developers = GetEmployeesSerializer(many=True, required=False)
    manager = GetEmployeesSerializer(many=False, required=False)

    base_namespace = GetNamespacesSerializer(many=False, required=False)
    base_chat_id = GetChatsSerializer(many=False, required=False)

    class Meta:
        model = ProductsModel
        exclude = ("updated", "deleted")
