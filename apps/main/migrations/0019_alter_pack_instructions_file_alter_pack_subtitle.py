# Generated by Django 4.2.3 on 2024-05-02 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_pack_instructions_file_alter_pack_subtitle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='instructions_file',
            field=models.FileField(upload_to='instructions', verbose_name='Archivo de instrucciones'),
        ),
        migrations.AlterField(
            model_name='pack',
            name='subtitle',
            field=models.CharField(default='', max_length=100, verbose_name='Subtítulo'),
        ),
    ]