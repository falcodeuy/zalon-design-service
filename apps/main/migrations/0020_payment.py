# Generated by Django 4.2.3 on 2024-05-02 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_pack_instructions_file_alter_pack_subtitle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Fecha de creación')),
                ('last_modified', models.DateTimeField(verbose_name='Última modificación')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=6, verbose_name='Monto')),
                ('payment_method', models.CharField(max_length=100, verbose_name='Método de pago')),
                ('payment_type', models.CharField(max_length=100, verbose_name='Tipo de pago')),
                ('payment_status', models.CharField(max_length=100, verbose_name='Estado de pago')),
                ('payment_id', models.CharField(max_length=100, verbose_name='ID de pago')),
                ('payment_provider', models.CharField(max_length=100, verbose_name='Proveedor de pago')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='main.order', verbose_name='Orden')),
            ],
        ),
    ]
