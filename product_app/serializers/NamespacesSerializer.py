from rest_framework import serializers

from product_app.models import NamespacesModel


class NamespacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamespacesModel
        fields = "__all__"

    # self.initial_data - хранит все переданные параметры
    def validate_product(self, value):
        # return NamespacesModel.objects.get(id=value).id
        return value
        # if self.initial_data.product == 1:
        #     raise serializers.ValidationError("product = 1")
        # return value

    # def get_product(self, instance):
    #     instance.product = NamespacesModel.objects.get(id=instance.product).name
