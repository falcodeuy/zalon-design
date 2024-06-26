# Generated by Django 4.2.3 on 2024-03-31 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_customerreview_options_alter_pack_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='pack',
            name='strikethrough_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True, verbose_name='Precio tachado'),
        ),
        migrations.AlterField(
            model_name='illustration',
            name='pack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='illustrations', to='main.pack', verbose_name='Pack'),
        ),
    ]
