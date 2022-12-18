from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from product_app.models import ChatsModel
from product_app.serializers.ChatsSerializer import ChatsSerializer


class ChatsViewSets(ModelViewSet):  # viewsets.ViewSet
    # queryset = EventTypesModel.objects.all()
    serializer_class = ChatsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []
    search_fields = []

    # override get queryset
    def get_queryset(self):
        return ChatsModel.objects.all()

    # business logic create object
    def perform_create(self, serializer):
        serializer.save()
        pass
