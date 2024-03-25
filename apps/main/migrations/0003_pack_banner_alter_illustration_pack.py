# Generated by Django 4.2.3 on 2024-03-25 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_illustration_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='pack',
            name='banner',
            field=models.ImageField(null=True, upload_to='banners', verbose_name='Banner'),
        ),
        migrations.AlterField(
            model_name='illustration',
            name='pack',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='illustrations', to='main.pack', verbose_name='Pack'),
        ),
    ]
