# Generated by Django 4.2.3 on 2024-06-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_pack_custom_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='subtitle',
            field=models.CharField(default='', max_length=350, verbose_name='Descripción corta'),
        ),
    ]