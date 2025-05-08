import csv
from django.core.management.base import BaseCommand
from news_app.models import VisualContent, Article

class Command(BaseCommand):
    help = "Load visual content from CSV file into the database"

    def handle(self, *args, **kwargs):
        file_path = "data/visualcontent.csv"  

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                article = None
                if row["Article ID"]:
                    try:
                        article = Article.objects.get(article_id=row["Article ID"])
                    except Article.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Article ID {row['Article ID']} not found, skipping."))

                visual, created = VisualContent.objects.get_or_create(
                    name=row["Name"],
                    file_url=row["File URL"],
                    file_type=row["File Type"],
                    css_class=row.get("CSS Class", ""), 
                    article=article,
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added: {visual.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Skipped (already exists): {visual.name}"))
