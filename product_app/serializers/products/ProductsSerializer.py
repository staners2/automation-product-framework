from rest_framework import serializers

from product_app.models.ProductsModel import ProductsModel
from product_app.serializers.ChatsSerializer import ChatsSerializer
from product_app.serializers.EmployeesSerializer import EmployeesSerializer
from product_app.serializers.NamespacesSerializer import NamespacesSerializer


class ProductsSerializer(serializers.ModelSerializer):

    namespaces = NamespacesSerializer(many=True, required=False)
    chats = ChatsSerializer(many=True, required=False)
    employees = EmployeesSerializer(many=True, required=False)

    base_namespace = NamespacesSerializer(many=False, required=False)
    base_chat_id = ChatsSerializer(many=False, required=False)

    class Meta:
        model = ProductsModel
        fields = "__all__"
