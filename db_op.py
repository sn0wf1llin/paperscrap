__author__ = 'MA573RWARR10R'
import sqlite3


def create_db(name):
    if '.sqlite3' not in name:
        sq_db_file = name + '.sqlite3'
    else:
        sq_db_file = name

    table_name = 'articles'  # name of the table to be created
    article_title = 'title'
    article_text = 'text'
    article_url = 'url'
    article_date = 'date'
    article_time = 'time'
    article_author = 'author'
    article_social_network = 'social'
    article_reposts = 'reposts'
    article_likes = 'likes'
    article_comments = 'comments'
    article_last_update_time = 'updatetime'

    conn = sqlite3.connect(sq_db_file)
    conn.text_factory = str

    conn.execute(
        "CREATE TABLE articles ({1} VARCHAR, {2} VARCHAR, {3} VARCHAR, {4} DATE, {5} TIME, {6} VARCHAR, {7} VARCHAR, {8} INTEGER , {9} INTEGER , {10} INTEGER , {11} VARCHAR )".format(
            table_name,
            article_title,
            article_text,
            article_url,
            article_date,
            article_time,
            article_author,
            article_social_network,
            article_reposts,
            article_likes,
            article_comments,
            article_last_update_time))
    conn.commit()

    print("Created successfully!")


def clear_db_table(db_name, table_name):
    if '.sqlite3' not in db_name:
        sq_db_file = db_name + '.sqlite3'
    else:
        sq_db_file = db_name

    conn = sqlite3.connect(sq_db_file)
    conn.text_factory = str

    conn.execute("DELETE FROM {0}".format(table_name))
    conn.commit()

    print("Deleted successfully!")

