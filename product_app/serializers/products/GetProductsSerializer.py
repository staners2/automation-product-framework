from rest_framework import serializers

from product_app.models.ProductsModel import ProductsModel
from product_app.serializers.chats.GetChatsSerializer import GetChatsSerializer
from product_app.serializers.employees.GetEmployeesSerializer import GetEmployeesSerializer
from product_app.serializers.namespaces.GetNamespacesSerializer import GetNamespacesSerializer


class GetProductsSerializer(serializers.ModelSerializer):

    namespaces = GetNamespacesSerializer(many=True, required=False)
    chats = GetChatsSerializer(many=True, required=False)
    employees = GetEmployeesSerializer(many=True, required=False)

    base_namespace = GetNamespacesSerializer(many=False, required=False)
    base_chat_id = GetChatsSerializer(many=False, required=False)

    class Meta:
        model = ProductsModel
        fields = "__all__"
