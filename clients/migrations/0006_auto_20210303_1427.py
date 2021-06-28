# Generated by Django 3.1.7 on 2021-03-03 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0005_auto_20210303_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='broker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='broker', to=settings.AUTH_USER_MODEL),
        ),
    ]
