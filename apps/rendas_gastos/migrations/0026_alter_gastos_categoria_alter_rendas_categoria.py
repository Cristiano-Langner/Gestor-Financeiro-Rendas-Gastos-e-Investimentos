# Generated by Django 4.2.4 on 2023-11-03 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendas_gastos', '0025_alter_gastos_data_alter_rendas_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastos',
            name='categoria',
            field=models.CharField(choices=[('Aluguel', 'Aluguel'), ('Mercado', 'Mercado'), ('Luz', 'Luz'), ('Água', 'Água'), ('Gás', 'Gás'), ('Gasolina', 'Gasolina'), ('Pet', 'Pet'), ('Internet', 'Internet'), ('Celular', 'Celular'), ('Lanches', 'Lanches'), ('Saúde', 'Saúde'), ('Transporte', 'Transporte'), ('Educação', 'Educação'), ('Assinaturas', 'Assinaturas'), ('Viagens', 'Viajens'), ('Vestuário', 'Vestuário'), ('Investimentos', 'Investimentos'), ('Doações', 'Doações'), ('Carro', 'Carro'), ('Seguros', 'Seguros'), ('Restaurante', 'Restaurante'), ('Casa', 'Casa'), ('Presente', 'Presente'), ('Outros', 'Outros')], default='Outros', max_length=100),
        ),
        migrations.AlterField(
            model_name='rendas',
            name='categoria',
            field=models.CharField(choices=[('Salário', 'Salário'), ('VA_VR', 'Va Vr'), ('Freela', 'Freela'), ('Venda ativos', 'Venda Ativos'), ('Cashback', 'Cashback'), ('Outros', 'Outros')], default='Outros', max_length=100),
        ),
    ]
