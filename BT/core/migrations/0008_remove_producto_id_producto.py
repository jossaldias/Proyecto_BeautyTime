# Generated by Django 4.2.1 on 2024-11-07 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_producto_costo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='id_producto',
        ),
    ]