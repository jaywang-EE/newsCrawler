from django.core.management.base import BaseCommand, CommandError
from news.crawler import craw

class Command(BaseCommand):
    help = 'start crawl'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        craw()
        self.stdout.write(self.style.SUCCESS('Successfully crawl'))
        """
        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            """