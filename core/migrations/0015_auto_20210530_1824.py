# Generated by Django 3.1.7 on 2021-05-30 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210505_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='name',
            field=models.CharField(error_messages={'unique': 'Bank with this name already exists'}, max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='bankcombinations',
            name='challenge',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='challenge_combinations', to='core.challenge'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankcombinations',
            name='solution',
            field=models.TextField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
