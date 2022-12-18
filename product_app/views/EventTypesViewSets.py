from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from product_app.models.EventTypesModel import EventTypesModel
from product_app.serializers.EventTypesSerializer import EventTypesSerializer


class EventTypesViewSets(ModelViewSet):  # viewsets.ViewSet
    # queryset = EventTypesModel.objects.all()
    serializer_class = EventTypesSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["point"]
    search_fields = [""]

    # override get queryset
    def get_queryset(self):
        return EventTypesModel.objects.all()

    # business logic create object
    def perform_create(self, serializer):
        serializer.save()
        pass

    # def list(self, request):
    #     event_types = EventTypesModel.objects.all()
    #     return event_types
    #
    #
    # def create(self, request):
    #     pass
    #
    # def retrieve(self, request, pk=None):
    #     pass
    #
    # def update(self, request, pk=None):
    #     pass
    #
    # def destroy(self, request, pk=None):
    #     pass
