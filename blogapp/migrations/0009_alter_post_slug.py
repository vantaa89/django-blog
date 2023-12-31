# Generated by Django 5.0 on 2024-01-01 02:17

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blogapp", "0008_post_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=True, populate_from="title", unique=True
            ),
        ),
    ]
