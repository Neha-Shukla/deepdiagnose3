# Generated by Django 2.1.5 on 2019-02-17 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deep_diagnose', '0011_auto_20190212_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]