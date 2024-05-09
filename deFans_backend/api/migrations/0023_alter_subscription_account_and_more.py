# Generated by Django 4.0.10 on 2024-05-08 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.account'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='creator',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.creator'),
        ),
    ]
