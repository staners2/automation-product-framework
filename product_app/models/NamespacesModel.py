from django.db import models

from product_app.models.ProductsModel import ProductsModel


class NamespacesModel(models.Model):
    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    product = models.ForeignKey(ProductsModel, related_name="namespaces", on_delete=models.CASCADE, help_text="Продукт")
    name = models.TextField(name="name", help_text="Название пространства Jira")

    def natural_key(self):
        return "fsdfsdf"

    # Metadata
    class Meta:
        db_table = "namespaces"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
