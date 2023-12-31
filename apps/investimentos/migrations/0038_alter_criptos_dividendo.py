# Generated by Django 4.2.4 on 2023-11-28 09:36

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investimentos', '0037_alter_criptos_preco_medio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criptos',
            name='dividendo',
            field=models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=14, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
