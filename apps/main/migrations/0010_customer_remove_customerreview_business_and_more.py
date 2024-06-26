# Generated by Django 4.2.3 on 2024-04-14 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_pack_strikethrough_price_alter_illustration_pack'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('business', models.CharField(max_length=100, verbose_name='Empresa')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=100, verbose_name='Teléfono')),
            ],
        ),
        migrations.RemoveField(
            model_name='customerreview',
            name='business',
        ),
        migrations.RemoveField(
            model_name='customerreview',
            name='name',
        ),
        migrations.AlterField(
            model_name='customerreview',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='reviews', verbose_name='Imagen'),
        ),
        migrations.CreateModel(
            name='PackSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='main.customer', verbose_name='Cliente')),
                ('pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pack', verbose_name='Pack')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
            },
        ),
        migrations.AddField(
            model_name='customerreview',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.customer', verbose_name='Cliente'),
            preserve_default=False,
        ),
    ]
