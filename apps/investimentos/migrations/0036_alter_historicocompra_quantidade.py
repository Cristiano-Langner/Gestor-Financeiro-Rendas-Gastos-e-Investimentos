# Generated by Django 4.2.4 on 2023-11-08 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0035_alter_acoes_valor_alter_bdrs_valor_alter_fiis_valor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicocompra',
            name='quantidade',
            field=models.IntegerField(default=0),
        ),
    ]
