# Generated by Django 4.2.4 on 2023-09-25 19:40

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0015_alter_acoes_quantidade_alter_bdrs_quantidade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acoes',
            name='valor',
            field=models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='bdrs',
            name='valor',
            field=models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='criptos',
            name='valor',
            field=models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='fiis',
            name='valor',
            field=models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='rendasfixa',
            name='valor',
            field=models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
