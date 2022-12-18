from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from product_app.models.EmployeesModel import EmployeesModel
from product_app.serializers.EmployeesSerializer import EmployeesSerializer


class EmployeesViewSets(ModelViewSet):  # viewsets.ViewSet
    # queryset = EventTypesModel.objects.all()
    serializer_class = EmployeesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    search_fields = []

    # override get queryset
    def get_queryset(self):
        return EmployeesModel.objects.all()

    # business logic create object
    def perform_create(self, serializer):
        serializer.save()
        pass
