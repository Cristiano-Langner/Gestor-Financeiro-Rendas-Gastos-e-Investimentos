# Generated by Django 4.2.4 on 2023-08-28 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rendas_gastos', '0012_alter_gastos_data_alter_rendas_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gastos',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='rendas',
            name='descricao',
        ),
    ]
