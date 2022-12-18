from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from product_app.models import NamespacesModel
from product_app.serializers.NamespacesSerializer import NamespacesSerializer


class NamespacesViewSets(ModelViewSet):  # viewsets.ViewSet
    # queryset = EventTypesModel.objects.all()
    serializer_class = NamespacesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    search_fields = []

    # override get queryset
    def get_queryset(self):
        return NamespacesModel.objects.all()

    # business logic create object
    def perform_create(self, serializer):
        serializer.save()

    #
    # def create(self, request, *args, **kwargs):
    #     serializers = self.get_serializer(data=request.data)
    #     serializers.is_valid(raise_exception=True)
    #     raise Exception(serializers.data)
    #     self.perform_create(serializers)
    #     headers = self.get_success_headers(serializers.data)
    #     return Response(serializers.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializers):
    #     serializers.save()
    #
    # def get_success_headers(self, data):
    #     try:
    #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         return {}
