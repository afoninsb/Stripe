# Generated by Django 4.1.6 on 2023-02-12 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_item_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.tax', verbose_name='Налог'),
        ),
    ]
