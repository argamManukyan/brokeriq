# Generated by Django 3.1.7 on 2021-03-04 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210303_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challange',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]