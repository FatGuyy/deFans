# Generated by Django 4.0.10 on 2024-04-24 02:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0015_remove_account_subscribed_account_subscriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscriptions', to='api.creator'),
        ),
        migrations.AlterField(
            model_name='creator',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
    ]
