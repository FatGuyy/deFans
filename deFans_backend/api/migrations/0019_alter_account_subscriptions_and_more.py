# Generated by Django 4.0.10 on 2024-04-24 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_creator_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, related_name='subscribed_creators', to='api.creator'),
        ),
        migrations.AlterField(
            model_name='creator',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribed_accounts', to='api.account'),
        ),
    ]
