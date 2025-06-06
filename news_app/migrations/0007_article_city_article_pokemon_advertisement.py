# Generated by Django 5.1.6 on 2025-04-20 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_article_image_filename_article_video_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='pokemon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=255)),
                ('file_url', models.URLField()),
                ('file_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=10)),
                ('css_class', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to='news_app.article')),
            ],
        ),
    ]
