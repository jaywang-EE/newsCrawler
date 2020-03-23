import random
  
from django.core.management.base import BaseCommand
from django.core.cache import cache
  
class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        自定義命令
        :return:
        """
        seed = "123456789"
        sa = []
        for i in range(4):
          sa.append(random.choice(seed))
        code = ''.join(sa)
        cache.set("test_"+code, code)

        print("test_"+code)

