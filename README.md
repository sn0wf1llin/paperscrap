paperscrap
===
Code for scrapping papermag.com & store in DB.

#### Project uses `redis` for parsing pages asynchronously.

**You need [redis](https://pypi.python.org/pypi/redis) and [redis-server](https://redis.io/topics/quickstart) to be installed**

`pars.py` - parses site and store urls in papermag_urls.txt;

`page.py` - parses one url & returns dict with data;

`initiator.py` - initiate queue in Redis with urls from papermag_urls.txt;

`processor.py` - worker process, takes url from queue and processes it;
you need execute **several** workers for asynchronously pages scrapping;

1. Collect urls and save them in papermag_urls.txt;
2. Initiate Redis queue with them;
3. Execute for example 5 processes, and wait for filling you database with collected data.