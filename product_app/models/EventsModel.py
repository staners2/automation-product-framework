from django.db import models
from rest_framework.generics import GenericAPIView

from product_app.models.EventTypesModel import EventTypesModel
from product_app.models.ProductsModel import ProductsModel


class EventsModel(models.Model):
    GenericAPIView
    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    type = models.ForeignKey(EventTypesModel, related_name="types", on_delete=models.CASCADE, help_text="Тип события")
    product = models.ForeignKey(ProductsModel, related_name="event", on_delete=models.CASCADE, help_text="Продукт")
    date = models.DateField(name="date", help_text="Дата проведения события")
    url = models.URLField(name="url", null=True, help_text="Ссылка на задачу в Jira")
    description = models.TextField(name="description", null=True, help_text="Название события")

    # Metadata
    class Meta:
        db_table = "events"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.type.title} | {self.product.name} | {self.date} | {self.url} | {self.description}"
