from rest_framework import serializers

from product_app.models.EmployeesModel import EmployeesModel


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesModel
        fields = "__all__"
