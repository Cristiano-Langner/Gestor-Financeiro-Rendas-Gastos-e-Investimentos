# Generated by Django 4.2.4 on 2023-11-08 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rendas_gastos', '0026_alter_gastos_categoria_alter_rendas_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='gastos',
            name='descricao',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AddField(
            model_name='rendas',
            name='descricao',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AlterField(
            model_name='gastos',
            name='categoria',
            field=models.CharField(choices=[('Água', 'Água'), ('Aluguel', 'Aluguel'), ('Assinaturas', 'Assinaturas'), ('Carro', 'Carro'), ('Casa', 'Casa'), ('Celular', 'Celular'), ('Condomínio', 'Condomínio'), ('Doações', 'Doações'), ('Educação', 'Educação'), ('Gás', 'Gás'), ('Gasolina', 'Gasolina'), ('Investimentos', 'Investimentos'), ('Internet', 'Internet'), ('Lanches', 'Lanches'), ('Luz', 'Luz'), ('Mercado', 'Mercado'), ('Pet', 'Pet'), ('Presente', 'Presente'), ('Restaurante', 'Restaurante'), ('Saúde', 'Saúde'), ('Seguros', 'Seguros'), ('Transporte', 'Transporte'), ('Vestuário', 'Vestuário'), ('Viagens', 'Viagens'), ('Outros', 'Outros')], default='Outros', max_length=100),
        ),
    ]
