# Generated by Django 3.2.8 on 2023-08-21 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('imagen', models.ImageField(null=True, upload_to='imagenes/', verbose_name='Imagen')),
                ('marca', models.CharField(max_length=100, verbose_name='Marca')),
                ('categoria', models.CharField(max_length=100, verbose_name='Categoria')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('stock', models.PositiveIntegerField(verbose_name='Stock')),
            ],
        ),
    ]