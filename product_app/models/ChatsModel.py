from django.db import models

from product_app.models.ProductsModel import ProductsModel


class ChatsModel(models.Model):
    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    product = models.ForeignKey(ProductsModel, related_name="chats", on_delete=models.CASCADE, help_text="Продукт")
    name = models.TextField(name="name", help_text="Название пространства Jira")

    # Metadata
    class Meta:
        db_table = "chats"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
