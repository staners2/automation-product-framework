from django.db import models


class EmployeesModel(models.Model):
    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    login = models.TextField(name="login", help_text="Логин сотрудника")
    full_name = models.TextField(name="full_name", null=True, default=None, help_text="ФИО сотрудника")
    is_developer = models.BooleanField(name="is_developer", default=False, help_text="Разработчик продукта?")
    is_manager = models.BooleanField(name="is_manager", default=False, help_text="Руководитель продукта?")

    # Metadata
    class Meta:
        db_table = "employees"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.login
