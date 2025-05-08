import csv
from django.core.management.base import BaseCommand
from news_app.models import Article

class Command(BaseCommand):
    help = "Load articles from CSV file into the database"

    def handle(self, *args, **kwargs):
        file_path = "data/articles.csv"  

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                article, created = Article.objects.get_or_create(
                    article_id=row["id"],
                    headline=row["headline"],
                    content=row["content"].replace("\n", "\n"),  
                    image_url=row["image_url"],
                    video_url=row["video_url"],
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {article.headline}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped (already exists): {article.headline}"))
