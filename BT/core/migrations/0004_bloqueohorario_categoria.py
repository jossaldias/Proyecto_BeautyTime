# Generated by Django 5.1.1 on 2024-12-03 02:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_bloqueohorario"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloqueohorario",
            name="categoria",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bloqueos",
                to="core.categoria",
            ),
        ),
    ]