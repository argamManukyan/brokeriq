# Generated by Django 3.1.7 on 2021-05-05 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210505_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankcombinations',
            name='bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_combinations', to='core.bank'),
        ),
        migrations.AlterField(
            model_name='bankcombinations',
            name='challenge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='challenge_combinations', to='core.challenge'),
        ),
    ]
