from rest_framework import serializers

from product_app.models import PlansModel
from product_app.serializers.ProductsSerializer import ProductsSerializer


class UpdatePlansSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlansModel
        fields = "__all__"


    def validate_date(self, value):
        # print(self.instance.__dict__)
        # print(self.initial_data)
        # if (PlansModel.objects.filter(product=self.initial_data["product"], date=self.initial_data["date"], id=self.instance.id).count() != 0):
        #     raise serializers.ValidationError("План на этот месяц уже составлен")

        return value