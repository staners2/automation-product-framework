from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from web.models.EmployeesModel import EmployeesModel
from web.serializers.employees.CreateEmployeesSerializer import (
    CreateEmployeesSerializer,
)
from web.serializers.employees.GetEmployeesSerializer import GetEmployeesSerializer
from web.serializers.employees.UpdateEmployeesSerializer import (
    UpdateEmployeesSerializer,
)


class EmployeesViewSets(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = []  # type: ignore
    search_fields = []  # type: ignore

    # override get queryset
    def get_queryset(self):
        return EmployeesModel.objects.filter(deleted=None).all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetEmployeesSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetEmployeesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GetEmployeesSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateEmployeesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = UpdateEmployeesSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    # TODO: Проверять все продукты и удалять из их команды удаленного пользователя?
    def perform_destroy(self, instance):
        date = timezone.now()
        instance.deleted = date
        instance.updated = date
        instance.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)