# Generated by Django 4.1.6 on 2023-02-11 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='count',
        ),
    ]
