# Generated by Django 4.2.1 on 2024-11-04 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_tipo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='order',
            name='observaciones',
            field=models.CharField(blank=True, max_length=250, verbose_name='Observaciones'),
        ),
    ]