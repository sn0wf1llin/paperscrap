__author__ = 'MA573RWARR10R'
from db_op import clear_db_table
import redis
from page import get_info, sqlite_insert
import sqlite3


# clear_db_table("../sq.sqlite3", 'articles')
# exit()
#create_db("sq.sqlite3")

conn = sqlite3.connect("../sq.sqlite3")
conn.text_factory = str

rcon = redis.Redis()

def run():

    while True:
        url = rcon.blpop(['urls'],)[1]

        try:
            parsed_data = get_info(url)
            sqlite_insert(conn=conn, table='articles', row=parsed_data)

        except Exception as e:
            print("Trouble happened {0}".format(e))
            rcon.lpush('main', url)

run()
