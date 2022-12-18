from django.db import models


class ProductsModel(models.Model):

    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    name = models.TextField(name="name", help_text="Название продукта")
    base_namespace = models.TextField(name="base_namespace", help_text="Пространство Jira")
    base_chat_id = models.TextField(name="base_chat_id", help_text="Чат для отправки оповещений", default="")
    is_active = models.BooleanField(name="is_active", default=True, help_text="Проект активен?")

    # Metadata
    class Meta:
        db_table = "products"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.name} | {self.base_namespace} | {self.is_active}"
