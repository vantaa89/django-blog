# Generated by Django 5.0 on 2024-01-02 02:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blogapp", "0016_rename_image_post_images"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="images",
        ),
    ]
