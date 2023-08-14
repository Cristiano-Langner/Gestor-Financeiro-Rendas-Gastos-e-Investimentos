# Generated by Django 4.2.4 on 2023-08-14 12:30

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendas_gastos', '0002_delete_choicesgastos_delete_choicesrendas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastos',
            name='data',
            field=models.DateField(default=datetime.date(2023, 8, 14), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 14))]),
        ),
        migrations.AlterField(
            model_name='rendas',
            name='data',
            field=models.DateField(default=datetime.date(2023, 8, 14), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 14))]),
        ),
    ]
