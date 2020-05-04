from django.core.management.base import BaseCommand, CommandError
from news.models import News

class Command(BaseCommand):
    help = 'update old source'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        news = News.objects.filter(source__isnull=True)
        print("Adding %d sources..."%news.count())

        for nw in news:
            if nw.category in ("food", "corporations", "climate"):
                source = "treehugger"
            elif nw.category == "msc":
                source = "vice"
            elif nw.category == "buddies":
                source = "thedodo"
            else:
                source = None

            if source:
                nw.source = source
                nw.save()
        """
        craw()
        self.stdout.write(self.style.SUCCESS('Successfully crawl'))
        """