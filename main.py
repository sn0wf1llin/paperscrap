__author__ = 'MA573RWARR10R'
from page import sqlite_insert
from db_op import clear_db_table, create_db
from pars import get_urls_from_doc
import sqlite3
from page import get_info
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures


#clear_db_table("sq.sqlite3", 'articles')
# create_db("sq.sqlite3")
# exit()

urls = get_urls_from_doc('papermag_urls.txt')
url = "http://www.paperscrap/2159606946.html"
print(url)

parsed_data = get_info(url)

# conn = sqlite3.connect("sq.sqlite3")
# conn.text_factory = str
#
# with ProcessPoolExecutor(max_workers=5) as executor:
#     future_results = {
#         executor.submit(get_info, url):
#             url for url in urls
#     }
#
#     results = []
#
#     for future in concurrent.futures.as_completed(future_results):
#         sqlite_insert(conn=conn, table='articles', row=future.result())
#
#         print("saved: {0}".format(future.result()['title']))
