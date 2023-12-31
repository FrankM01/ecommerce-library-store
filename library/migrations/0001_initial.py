# Generated by Django 3.2.8 on 2023-10-19 00:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import library.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, validators=[library.validators.validate_cate_length, library.validators.validate_cate_letters_only], verbose_name='Categoria')),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=51, validators=[library.validators.validate_nombre_length, library.validators.validate_nombre], verbose_name='Nombre')),
                ('imagen', models.ImageField(null=True, upload_to=library.validators.custom_upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']), library.validators.validate_image_size], verbose_name='Imagen')),
                ('marca', models.CharField(max_length=100, null=True, validators=[library.validators.validate_marca_length, library.validators.validate_marca_letters_only], verbose_name='Marca')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[library.validators.validate_precio], verbose_name='Precio')),
                ('stock', models.PositiveIntegerField(null=True, validators=[library.validators.validate_stock_range, library.validators.validate_stock_positive], verbose_name='Stock')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='library.categoria')),
            ],
        ),
    ]
