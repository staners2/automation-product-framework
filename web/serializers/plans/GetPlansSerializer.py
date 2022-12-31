from rest_framework import serializers

from web.models.PlansModel import PlansModel
from web.serializers.products.GetProductsSerializer import GetProductsSerializer


class GetPlansSerializer(serializers.ModelSerializer):

    product = GetProductsSerializer(many=False)

    class Meta:
        model = PlansModel
        exclude = ("updated", "deleted")
