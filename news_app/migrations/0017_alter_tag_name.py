# Generated by Django 5.1.6 on 2025-05-07 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0016_alter_profile_favorite_creators_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
