from django.db import models

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
    employees = models.ManyToManyField(EmployeesModel, related_name="employees", null=True)
    namespaces = models.ManyToManyField(NamespacesModel, related_name="namespaces", null=True)
    chats = models.ManyToManyField(ChatsModel, related_name="chats", null=True)
    is_active = models.BooleanField(name="is_active", default=True, help_text="Проект активен?")

    # Metadata
    class Meta:
        db_table = "products"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.title} | {self.base_namespace} | {self.is_active}"
