# Generated by Django 3.1.7 on 2021-03-03 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210303_1021'),
        ('clients', '0004_auto_20210303_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientchallangeandsolution',
            name='solution',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.solution'),
        ),
    ]
