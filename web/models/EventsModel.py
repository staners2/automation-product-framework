from django.db import models
from django.utils import timezone

from web.models.EmployeesModel import EmployeesModel
from web.models.EventTypesModel import EventTypesModel
from web.models.ProductsModel import ProductsModel


class EventsModel(models.Model):
    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    type = models.ForeignKey(EventTypesModel, related_name="types", on_delete=models.CASCADE, help_text="Тип события")
    product = models.ForeignKey(ProductsModel, related_name="event", on_delete=models.CASCADE, help_text="Продукт")
    assignee = models.ForeignKey(
        EmployeesModel,
        related_name="assignee",
        default=None,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Исполнитель",
    )
    date = models.DateField(name="date", help_text="Дата проведения события")
    url = models.URLField(name="url", null=True, help_text="Ссылка на задачу в Jira")
    description = models.TextField(name="description", default=None, null=True, help_text="Название события")
    updated = models.DateTimeField(name="updated", help_text="Время обновления", default=timezone.now)
    deleted = models.DateTimeField(name="deleted", help_text="Время удаления", default=None, blank=True, null=True)

    # Metadata
    class Meta:
        db_table = "actions"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.type.title} | {self.product.title} | {self.assignee} | {self.date} | {self.url} | {self.description}"
