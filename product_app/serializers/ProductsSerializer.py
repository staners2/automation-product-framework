from rest_framework import serializers

from product_app.models import ProductsModel
from product_app.serializers.ChatsSerializer import ChatsSerializer
from product_app.serializers.EmployeesSerializer import EmployeesSerializer
from product_app.serializers.NamespacesSerializer import NamespacesSerializer


class ProductsSerializer(serializers.ModelSerializer):

    namespaces = NamespacesSerializer(many=True)
    chats = ChatsSerializer(many=True)
    employees = EmployeesSerializer(many=True)

    class Meta:
        model = ProductsModel
        fields = "__all__"
