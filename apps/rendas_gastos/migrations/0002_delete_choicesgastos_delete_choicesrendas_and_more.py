# Generated by Django 4.2.4 on 2023-08-12 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rendas_gastos', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ChoicesGastos',
        ),
        migrations.DeleteModel(
            name='ChoicesRendas',
        ),
        migrations.DeleteModel(
            name='Transacao',
        ),
    ]
