# Generated by Django 4.0.10 on 2024-04-17 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_account_subscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='coverPhoto',
            field=models.ImageField(blank=True, upload_to='Account_cover_photos'),
        ),
        migrations.AlterField(
            model_name='account',
            name='profilePhoto',
            field=models.ImageField(blank=True, upload_to='Account_Profile_photos'),
        ),
        migrations.AlterField(
            model_name='creator',
            name='coverPhoto',
            field=models.ImageField(blank=True, upload_to='Creator_Cover_photos'),
        ),
        migrations.AlterField(
            model_name='creator',
            name='profilePhoto',
            field=models.ImageField(blank=True, upload_to='Creator_Profile_photos'),
        ),
    ]
