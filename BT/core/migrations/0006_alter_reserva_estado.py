# Generated by Django 5.1.1 on 2024-12-09 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_alter_bloqueohorario_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reserva",
            name="estado",
            field=models.CharField(
                choices=[
                    ("confirmado", "Confirmado"),
                    ("pendiente", "Pendiente"),
                    ("eliminado", "Eliminado"),
                    ("enConflicto", "En Conflicto"),
                ],
                default="pendiente",
                max_length=12,
            ),
        ),
    ]
