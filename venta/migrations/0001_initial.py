# Generated by Django 4.2.1 on 2024-01-01 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid
import venta.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producto', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default=uuid.uuid4, editable=False, max_length=100, unique=True)),
                ('estado', models.CharField(choices=[('1', 'Activo'), ('0', 'Inactivo')], default='1', max_length=1, verbose_name='Estado')),
                ('fecha_creacion', models.DateField(auto_now=True, verbose_name='Fecha de Creación')),
                ('Cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Cliente', to='cliente.cliente', verbose_name='Cliente')),
                ('Empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Detalleventa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(validators=[venta.models.validate_positive], verbose_name='cantidad')),
                ('valortotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='valor total')),
                ('estado', models.CharField(choices=[('1', 'Activo'), ('0', 'Inactivo')], default='1', max_length=1, verbose_name='Estado')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.venta', verbose_name='Grupo')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='producto.producto', verbose_name='Producto')),
            ],
        ),
    ]
