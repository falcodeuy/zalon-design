# Generated by Django 4.2.3 on 2024-05-03 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_payment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Teléfono'),
        ),
    ]