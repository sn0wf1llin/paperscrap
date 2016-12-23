__author__ = 'MA573RWARR10R'
from pars import get_urls_from_doc
import redis


rcon = redis.Redis()

def init_worker():

    urls = get_urls_from_doc('../papermag_urls.txt')

    for url in urls:
        rcon.lpush('urls', url)

init_worker()
