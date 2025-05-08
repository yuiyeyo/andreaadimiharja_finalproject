from django.core.management.base import BaseCommand
from news_app.models import Article
import csv
from django.utils.dateparse import parse_datetime


from django.core.management.base import BaseCommand
import csv
from news_app.models import Article

class Command(BaseCommand):
    help = 'Import articles from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        Article.objects.all().delete()

        csv_path = kwargs['csv_path']
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Article.objects.create(
                    article_id=row.get("id"),
                    headline=row.get("headline"),
                    content=row.get("content"),  
                    image_url=row.get("image_url"),
                    video_url=row.get("video_url"),
                    pokemon=row.get('pokemon') or None,
                    city=row.get('city') or None,
                )

        self.stdout.write(self.style.SUCCESS(f'Articles imported from {csv_path}'))
