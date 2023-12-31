# Generated by Django 4.2.4 on 2023-10-19 13:13

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investimentos', '0025_alter_historicocompra_quantidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='RendasFixaConsolidadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('quantidade', models.PositiveIntegerField(default=0)),
                ('preco_medio', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('dividendo', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('valor', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('lucro', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Rendas fixa consolidadas',
            },
        ),
    ]
