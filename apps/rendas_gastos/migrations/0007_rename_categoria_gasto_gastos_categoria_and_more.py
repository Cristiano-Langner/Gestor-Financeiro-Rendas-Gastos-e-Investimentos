# Generated by Django 4.2.4 on 2023-08-18 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rendas_gastos', '0006_alter_gastos_data_alter_rendas_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gastos',
            old_name='categoria_gasto',
            new_name='categoria',
        ),
        migrations.RenameField(
            model_name='rendas',
            old_name='categoria_renda',
            new_name='categoria',
        ),
    ]
