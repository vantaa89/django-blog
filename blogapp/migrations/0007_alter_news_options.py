# Generated by Django 5.0 on 2023-12-31 23:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blogapp", "0006_rename_update_news"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="news",
            options={"verbose_name_plural": "News"},
        ),
    ]
