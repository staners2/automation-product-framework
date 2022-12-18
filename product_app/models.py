from datetime import datetime

from django.db import models
from datetime import date
from django.utils.translation import gettext as _

# Create your samples here.


class EventTypesModel(models.Model):

    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    title = models.TextField(name="title", help_text="Название события")
    point = models.DecimalField(
        name="point", decimal_places=2, max_digits=5, help_text="Кол-во баллов за тип события", default=0.0
    )
    description = models.TextField(name="description", help_text="Описание события", default="")

    # Metadata
    class Meta:
        db_table = "event-types"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.title} | {self.point} | {self.description}"


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


class EventsModel(models.Model):

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


class PlansModel(models.Model):

    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    product = models.ForeignKey(ProductsModel, related_name="plans", on_delete=models.CASCADE, help_text="Продукт")
    date = models.DateField(name="date", default=date.today, help_text="День когда была сделана запись плана")
    daily = models.DecimalField(name="daily", decimal_places=2, max_digits=5, help_text="Дейли", default=0.0)
    review_code = models.DecimalField(
        name="review_code", decimal_places=2, max_digits=5, help_text="Ревью кода", default=0.0
    )
    one_to_one = models.DecimalField(
        name="one_to_one", decimal_places=2, max_digits=5, help_text="Один на один", default=0.0
    )
    individual_plan = models.DecimalField(
        name="individual_plan", decimal_places=2, max_digits=5, help_text="ПИР", default=0.0
    )
    meeting_on_product = models.DecimalField(
        name="meeting_on_product",
        decimal_places=2,
        max_digits=5,
        help_text="Встреча владельца продукта с Полетаевой",
        default=0.0,
    )
    close_task = models.DecimalField(
        name="close_task", decimal_places=2, max_digits=5, help_text="Закрытие задач", default=0.0
    )

    # Metadata
    class Meta:
        db_table = "plans"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f"{self.product.name} | {self.date}"


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


class EmployeesModel(models.Model):
    # Fields
    id = models.BigAutoField(name="id", primary_key=True)
    product = models.ForeignKey(ProductsModel, related_name="employees", on_delete=models.CASCADE, help_text="Продукт")
    login = models.TextField(name="login", help_text="Логин сотрудника")
    full_name = models.TextField(name="full_name", help_text="ФИО сотрудника")
    is_developer = models.BooleanField(name="is_developer", default=False, help_text="Разработчик продукта?")
    is_manager = models.BooleanField(name="is_manager", default=False, help_text="Руководитель продукта?")

    # Metadata
    class Meta:
        db_table = "employees"
        ordering = ["id"]

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.login
