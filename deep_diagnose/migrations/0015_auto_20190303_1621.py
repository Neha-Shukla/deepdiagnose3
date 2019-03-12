# Generated by Django 2.1.5 on 2019-03-03 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deep_diagnose', '0014_addtocart'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=125)),
            ],
        ),
        migrations.RemoveField(
            model_name='tests',
            name='test_details',
        ),
        migrations.AddField(
            model_name='tests',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='deep_diagnose.TestCategory'),
        ),
    ]
