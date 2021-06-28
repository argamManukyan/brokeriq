# Generated by Django 3.1.7 on 2021-05-20 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20210505_1018'),
        ('clients', '0012_auto_20210423_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienthistory',
            name='challenge_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='clienthistory',
            name='challenge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.challenge'),
        ),
        migrations.AlterField(
            model_name='clienthistory',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='history', to='clients.clients'),
        ),
        migrations.AlterField(
            model_name='clienthistory',
            name='solution',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='clients',
            name='best_matches',
        ),
        migrations.AddField(
            model_name='clients',
            name='best_matches',
            field=models.JSONField(null=True),
        ),
    ]