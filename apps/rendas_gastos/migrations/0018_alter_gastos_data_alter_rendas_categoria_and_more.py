# Generated by Django 4.2.4 on 2023-09-18 13:51

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendas_gastos', '0017_alter_gastos_categoria_alter_gastos_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastos',
            name='data',
            field=models.DateField(default=datetime.date(2023, 9, 18), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 9, 18))]),
        ),
        migrations.AlterField(
            model_name='rendas',
            name='categoria',
            field=models.CharField(choices=[('Salário', 'Salário'), ('Venda ativos', 'Venda Ativos'), ('Cashback', 'Cashback'), ('Outros', 'Outros')], default='Outros', max_length=100),
        ),
        migrations.AlterField(
            model_name='rendas',
            name='data',
            field=models.DateField(default=datetime.date(2023, 9, 18), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 9, 18))]),
        ),
    ]
