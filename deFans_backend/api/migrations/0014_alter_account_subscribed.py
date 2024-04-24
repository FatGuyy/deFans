# Generated by Django 4.0.10 on 2024-04-24 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_account_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='subscribed',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creators', to='api.creator'),
        ),
    ]