# Generated by Django 5.1.1 on 2024-10-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_item_cantidad_alter_item_categoria_alter_item_costo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('servicio', models.CharField(max_length=50)),
                ('contacto', models.CharField(blank=True, max_length=13, null=True)),
            ],
        ),
    ]