# Generated by Django 3.0.3 on 2020-02-27 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0002_auto_20200227_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='category',
            field=models.CharField(max_length=100),
        ),
    ]
