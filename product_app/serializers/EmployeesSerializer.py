from rest_framework import serializers

from product_app.models import EmployeesModel


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesModel
        fields = "__all__"
