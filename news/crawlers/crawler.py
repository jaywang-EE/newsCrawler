from datetime import datetime
from . import crawler_cases
from . import crawler_news
from . import utils

def craw_covid():
    cache = utils.open_cache()
    if ("last_update" not in cache or cache["last_update"] != datetime.now().strftime("%Y-%m-%d")):
        cache = {
            "county": crawler_cases.get_county_data(),
            "news": crawler_news.get_news(),
            "orders": crawler_news.craw_gov(),
            "last_update": datetime.now().strftime("%Y-%m-%d"),
        }
        utils.save_cache(cache)
    return cache

if __name__ == '__main__':
    craw_covid()