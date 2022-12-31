from rest_framework import serializers

from product_app.models.EmployeesModel import EmployeesModel


class GetEmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesModel
        exclude = ("updated", "deleted")
