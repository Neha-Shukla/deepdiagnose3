# Generated by Django 2.1.5 on 2019-03-16 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deep_diagnose', '0020_auto_20190316_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinfo',
            name='order_no',
        ),
    ]
