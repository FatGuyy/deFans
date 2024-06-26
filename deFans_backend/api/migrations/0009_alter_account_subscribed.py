# Generated by Django 4.0.10 on 2024-04-17 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_creator_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='subscribed',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='creators', to='api.creator'),
        ),
    ]
