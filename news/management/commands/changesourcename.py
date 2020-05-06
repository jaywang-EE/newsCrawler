from django.core.management.base import BaseCommand, CommandError
from news.models import News

class Command(BaseCommand):
    help = 'update old source'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        news = News.objects.filter(source="thedodo")
        print("Change %d sources..."%news.count())

        for nw in news:
            nw.source = "The Dodo"
            nw.save()
