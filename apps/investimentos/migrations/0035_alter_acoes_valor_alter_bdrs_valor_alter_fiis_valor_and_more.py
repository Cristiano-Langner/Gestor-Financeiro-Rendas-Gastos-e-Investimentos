# Generated by Django 4.2.4 on 2023-11-08 09:28

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0034_remove_rendasfixa_preco_medio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acoes',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='bdrs',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='fiis',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AlterField(
            model_name='rendasfixa',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
