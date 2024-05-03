# Generated by Django 4.2.3 on 2024-05-02 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_order_options_alter_order_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pack',
            name='show_in_landing',
        ),
        migrations.AddField(
            model_name='order',
            name='instructions_file',
            field=models.FileField(blank=True, null=True, upload_to='instructions', verbose_name='Archivo de instrucciones'),
        ),
    ]