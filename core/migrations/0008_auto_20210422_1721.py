# Generated by Django 3.1.7 on 2021-04-22 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210419_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]