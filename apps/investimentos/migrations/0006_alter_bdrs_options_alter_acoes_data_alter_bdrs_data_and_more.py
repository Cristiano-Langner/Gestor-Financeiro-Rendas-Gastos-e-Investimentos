# Generated by Django 4.2.4 on 2023-08-31 17:12

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investimentos', '0005_remove_acoes_nome_remove_bdrs_nome_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bdrs',
            options={'verbose_name_plural': 'BDRs'},
        ),
        migrations.AlterField(
            model_name='acoes',
            name='data',
            field=models.DateField(default=datetime.date(2023, 8, 31), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 31))]),
        ),
        migrations.AlterField(
            model_name='bdrs',
            name='data',
            field=models.DateField(default=datetime.date(2023, 8, 31), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 31))]),
        ),
        migrations.AlterField(
            model_name='criptos',
            name='data',
            field=models.DateField(default=datetime.date(2023, 8, 31), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 31))]),
        ),
        migrations.AlterField(
            model_name='fiis',
            name='data',
            field=models.DateField(default=datetime.date(2023, 8, 31), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 31))]),
        ),
        migrations.AlterField(
            model_name='rendasfixa',
            name='data',
            field=models.DateField(default=datetime.date(2023, 8, 31), validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 31))]),
        ),
        migrations.CreateModel(
            name='HistoricoDividendo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data', models.DateField()),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
