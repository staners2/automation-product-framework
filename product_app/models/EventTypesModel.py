from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class EventTypesModel(models.Model):

    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    title = models.TextField(name="title", help_text="Название события")
    point = models.DecimalField(
        name="point",
        decimal_places=2,
        max_digits=5,
        help_text="Кол-во баллов за тип события",
        validators=[MinValueValidator(Decimal("0"))],
        default=0.0,
    )
    description = models.TextField(name="description", default=None, null=True, help_text="Описание события")

    # Metadata
    class Meta:
        db_table = "event-types"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.title} | {self.point} | {self.description}"
