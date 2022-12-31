from rest_framework import serializers

from product_app.models.PlansModel import PlansModel
from product_app.serializers.products.GetProductsSerializer import GetProductsSerializer


class GetPlansSerializer(serializers.ModelSerializer):

    product = GetProductsSerializer(many=False)

    class Meta:
        model = PlansModel
        exclude = ("updated", "deleted")
