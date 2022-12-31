# Generated by Django 4.1.4 on 2022-12-31 02:15

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChatsModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.TextField(help_text="Название чата telegram")),
                ("chat_id", models.TextField(help_text="ID чата в telegram")),
                ("updated", models.DateTimeField(default=django.utils.timezone.now, help_text="Время обновления")),
                ("deleted", models.DateTimeField(blank=True, default=None, help_text="Время удаления", null=True)),
            ],
            options={
                "db_table": "chats",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="EmployeesModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("login", models.TextField(help_text="Логин сотрудника")),
                ("full_name", models.TextField(default=None, help_text="ФИО сотрудника", null=True)),
                ("is_developer", models.BooleanField(default=False, help_text="Разработчик продукта?")),
                ("is_manager", models.BooleanField(default=False, help_text="Руководитель продукта?")),
                ("updated", models.DateTimeField(default=django.utils.timezone.now, help_text="Время обновления")),
                ("deleted", models.DateTimeField(blank=True, default=None, help_text="Время удаления", null=True)),
            ],
            options={
                "db_table": "employees",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="EventTypesModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.TextField(help_text="Название события")),
                (
                    "point",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Кол-во баллов за тип события",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                ("description", models.TextField(default=None, help_text="Описание события", null=True)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now, help_text="Время обновления")),
                ("deleted", models.DateTimeField(blank=True, default=None, help_text="Время удаления", null=True)),
            ],
            options={
                "db_table": "event-types",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="NamespacesModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.TextField(help_text="Название пространства Jira")),
                ("updated", models.DateTimeField(default=django.utils.timezone.now, help_text="Время обновления")),
                ("deleted", models.DateTimeField(blank=True, default=None, help_text="Время удаления", null=True)),
            ],
            options={
                "db_table": "namespaces",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="ProductsModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("title", models.TextField(help_text="Название продукта")),
                ("is_active", models.BooleanField(default=True, help_text="Проект активен?")),
                ("updated", models.DateTimeField(default=django.utils.timezone.now, help_text="Время обновления")),
                ("deleted", models.DateTimeField(blank=True, default=None, help_text="Время удаления", null=True)),
                (
                    "base_chat_id",
                    models.ForeignKey(
                        blank=True,
                        help_text="Чат для отправки оповещений",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="base_chat_id",
                        to="web.chatsmodel",
                    ),
                ),
                (
                    "base_namespace",
                    models.ForeignKey(
                        blank=True,
                        help_text="Пространство Jira",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="base_namespaces",
                        to="web.namespacesmodel",
                    ),
                ),
                (
                    "chats",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        null=True,
                        related_name="chats",
                        to="web.chatsmodel",
                    ),
                ),
                (
                    "employees",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        null=True,
                        related_name="employees",
                        to="web.employeesmodel",
                    ),
                ),
                (
                    "namespaces",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        null=True,
                        related_name="namespaces",
                        to="web.namespacesmodel",
                    ),
                ),
            ],
            options={
                "db_table": "products",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="PlansModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("date", models.DateField(help_text="День когда была сделана запись плана")),
                (
                    "daily",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Дейли",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                (
                    "review_code",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Ревью кода",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                (
                    "one_to_one",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Один на один",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                (
                    "individual_plan",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="ПИР",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                (
                    "meeting_on_product",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Встреча владельца продукта с Полетаевой",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                (
                    "close_task",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        help_text="Закрытие задач",
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0"))],
                    ),
                ),
                ("updated", models.DateTimeField(default=django.utils.timezone.now, help_text="Время обновления")),
                ("deleted", models.DateTimeField(blank=True, default=None, help_text="Время удаления", null=True)),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Продукт",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plans",
                        to="web.productsmodel",
                    ),
                ),
            ],
            options={
                "db_table": "plans",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="EventsModel",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("date", models.DateField(help_text="Дата проведения события")),
                ("url", models.URLField(help_text="Ссылка на задачу в Jira", null=True)),
                ("description", models.TextField(default=None, help_text="Название события", null=True)),
                ("updated", models.DateTimeField(default=django.utils.timezone.now, help_text="Время обновления")),
                ("deleted", models.DateTimeField(blank=True, default=None, help_text="Время удаления", null=True)),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Исполнитель",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assignee",
                        to="web.employeesmodel",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="Продукт",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event",
                        to="web.productsmodel",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        help_text="Тип события",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="types",
                        to="web.eventtypesmodel",
                    ),
                ),
            ],
            options={
                "db_table": "actions",
                "ordering": ["id"],
            },
        ),
    ]
