from rest_framework import serializers

from product_app.models.EmployeesModel import EmployeesModel


class CreateEmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesModel
        fields = "__all__"

    def validate(self, attrs):
        if (
            EmployeesModel.objects.filter(
                login=self.initial_data["login"],
            ).count()
            != 0
        ):
            raise serializers.ValidationError("Пользователь с таким логином уже существует!")

        return attrs

    def create(self, validated_data):
        login = validated_data.get("login")
        full_name = validated_data.get("full_name", None)
        is_developer = validated_data.get("is_developer", False)
        is_manager = validated_data.get("is_manager", False)
        instance = EmployeesModel(login=login, full_name=full_name, is_developer=is_developer, is_manager=is_manager)
        instance.save()

        return instance
