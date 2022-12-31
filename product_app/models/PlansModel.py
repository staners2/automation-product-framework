from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from product_app.models.ProductsModel import ProductsModel


class PlansModel(models.Model):

    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    product = models.ForeignKey(ProductsModel, related_name="plans", on_delete=models.CASCADE, help_text="Продукт")
    date = models.DateField(name="date", help_text="День когда была сделана запись плана")
    daily = models.DecimalField(
        name="daily",
        decimal_places=2,
        max_digits=5,
        help_text="Дейли",
        validators=[MinValueValidator(Decimal("0"))],
        default=0.0,
    )
    review_code = models.DecimalField(
        name="review_code",
        decimal_places=2,
        max_digits=5,
        help_text="Ревью кода",
        validators=[MinValueValidator(Decimal("0"))],
        default=0.0,
    )
    one_to_one = models.DecimalField(
        name="one_to_one",
        decimal_places=2,
        max_digits=5,
        help_text="Один на один",
        validators=[MinValueValidator(Decimal("0"))],
        default=0.0,
    )
    individual_plan = models.DecimalField(
        name="individual_plan",
        decimal_places=2,
        max_digits=5,
        help_text="ПИР",
        validators=[MinValueValidator(Decimal("0"))],
        default=0.0,
    )
    meeting_on_product = models.DecimalField(
        name="meeting_on_product",
        decimal_places=2,
        max_digits=5,
        help_text="Встреча владельца продукта с Полетаевой",
        validators=[MinValueValidator(Decimal("0"))],
        default=0.0,
    )
    close_task = models.DecimalField(
        name="close_task",
        decimal_places=2,
        max_digits=5,
        help_text="Закрытие задач",
        validators=[MinValueValidator(Decimal("0"))],
        default=0.0,
    )
    updated = models.DateTimeField(name="updated", help_text="Время обновления", default=timezone.now)
    deleted = models.DateTimeField(name="deleted", help_text="Время удаления", default=None, blank=True, null=True)

    # Metadata
    class Meta:
        db_table = "plans"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.product.title} | {self.date}"
