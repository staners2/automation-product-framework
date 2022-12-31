from rest_framework import serializers

from web.models.EmployeesModel import EmployeesModel


class CreateEmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesModel
        exclude = ("updated", "deleted")

    def validate(self, attrs):
        if (
            EmployeesModel.objects.filter(
                login=attrs.get("login"),
                deleted=None,
            ).count()
            != 0
        ):
            raise serializers.ValidationError("Пользователь с таким логином уже существует!")

        return attrs

    def create(self, validated_data):
        login = validated_data.get("login")
        full_name = validated_data.get("full_name", None)
        instance = EmployeesModel(login=login, full_name=full_name)
        instance.save()

        return instance
