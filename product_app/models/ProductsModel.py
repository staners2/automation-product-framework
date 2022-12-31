from django.db import models
from django.utils import timezone

from product_app.models.ChatsModel import ChatsModel
from product_app.models.EmployeesModel import EmployeesModel
from product_app.models.NamespacesModel import NamespacesModel


class ProductsModel(models.Model):

    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    title = models.TextField(name="title", help_text="Название продукта")
    base_namespace = models.ForeignKey(
        NamespacesModel,
        related_name="base_namespaces",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Пространство Jira",
    )
    base_chat_id = models.ForeignKey(
        ChatsModel,
        related_name="base_chat_id",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="Чат для отправки оповещений",
    )
    employees = models.ManyToManyField(EmployeesModel, related_name="employees", null=True, blank=True, default=None)
    namespaces = models.ManyToManyField(NamespacesModel, related_name="namespaces", null=True, blank=True, default=None)
    chats = models.ManyToManyField(ChatsModel, related_name="chats", null=True, blank=True, default=None)
    is_active = models.BooleanField(name="is_active", default=True, help_text="Проект активен?")
    updated = models.DateTimeField(name="updated", help_text="Время обновления", default=timezone.now)
    deleted = models.DateTimeField(name="deleted", help_text="Время удаления", default=None, blank=True, null=True)

    # Metadata
    class Meta:
        db_table = "products"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.title} | {self.base_namespace} | {self.is_active}"
