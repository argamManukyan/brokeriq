# Generated by Django 3.1.7 on 2021-05-23 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0013_auto_20210520_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienthistory',
            name='combination_for_any_bak',
            field=models.JSONField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
