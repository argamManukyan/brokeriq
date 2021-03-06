# Generated by Django 3.1.7 on 2021-05-05 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210504_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(db_index=True, error_messages={'unique': 'Bank with this name already exists'}, max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='bankcombinations',
            name='coefficient',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bankcombinations',
            name='solution',
            field=models.TextField(blank=True, null=True),
        ),
    ]
