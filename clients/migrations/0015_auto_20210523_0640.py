# Generated by Django 3.1.7 on 2021-05-23 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_clienthistory_combination_for_any_bak'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clienthistory',
            old_name='combination_for_any_bak',
            new_name='combinations',
        ),
    ]
