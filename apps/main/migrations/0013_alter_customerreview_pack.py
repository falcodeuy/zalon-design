# Generated by Django 4.2.3 on 2024-04-25 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_customerreview_image_customer_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreview',
            name='pack',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='main.pack', verbose_name='Pack'),
            preserve_default=False,
        ),
    ]
