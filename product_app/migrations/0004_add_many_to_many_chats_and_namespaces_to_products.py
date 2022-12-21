# Generated by Django 4.1.4 on 2022-12-18 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product_app", "0003_set_min_value_plans_point"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="chatsmodel",
            name="product",
        ),
        migrations.RemoveField(
            model_name="namespacesmodel",
            name="product",
        ),
        migrations.AddField(
            model_name="productsmodel",
            name="chats",
            field=models.ManyToManyField(to="product_app.chatsmodel"),
        ),
        migrations.AddField(
            model_name="productsmodel",
            name="namespaces",
            field=models.ManyToManyField(to="product_app.namespacesmodel"),
        ),
        migrations.AlterField(
            model_name="productsmodel",
            name="base_chat_id",
            field=models.ForeignKey(
                help_text="Чат для отправки оповещений",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="base_chat_id",
                to="product_app.chatsmodel",
            ),
        ),
        migrations.AlterField(
            model_name="productsmodel",
            name="base_namespace",
            field=models.ForeignKey(
                help_text="Пространство Jira",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="base_namespaces",
                to="product_app.namespacesmodel",
            ),
        ),
    ]
