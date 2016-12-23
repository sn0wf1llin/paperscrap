__author__ = 'MA573RWARR10R'
import json
import requests
from bs4 import BeautifulSoup
import re
from tokens import access_token
from data_collector import FacebookDataCollector


def sqlite_insert(conn, table, row):
    cols = ', '.join('"{}"'.format(col) for col in row.keys())
    vals = ', '.join(':{}'.format(col) for col in row.keys())
    sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
    conn.cursor().execute(sql, row)
    conn.commit()


def make_request(host_, url_):
    res = requests.get(host_ + url_)

    return res.content


def get_readable_text(non_readable):
    rt = re.sub('<.*?>', '', non_readable)

    return rt


def get_info(url):
    article_content = make_request(url, '')
    soup = BeautifulSoup(article_content, "lxml")

    url_for_facebook = soup.find("meta", {'property': "og:url"})['content']

    title = get_readable_text(soup.find("div", {'class': "headline"}).text)

    text = ""
    try:
        for tag in soup.find("div", {'class': "article-description"}).find_all("p"):
            text += get_readable_text(tag.text)

        for tag in soup.find("div", {'class': "article-description"}).find_all("blockquote"):
            text += get_readable_text(tag.text)

    except AttributeError:
        pass

    try:
        collector = FacebookDataCollector('', access_token)
        collected_l = collector.get_data(url_for_facebook)

        social_brand = collected_l["social"]
        reposts = int(collected_l["reposts"])
        likes = int(collected_l["likes"])
        comments = int(collected_l["comments"])
        uptime = collected_l["updated_time"]

    except Exception as e:
        print("\t{0}".format(e))
        social_brand = "unknown"
        reposts = 0
        likes = 0
        comments = 0
        uptime = "unknown"

    author = get_readable_text(soup.find("a", {'class': "author-post__name"}).text)
    datetime = get_readable_text(soup.find("div", {'class': "author-post__date"}).text).split("at")

    date = datetime[0]
    time = datetime[1]

    return {
        'title': title,
        'text': text,
        'url': url_for_facebook,
        'likes': likes,
        'comments': comments,
        'author': author,
        'social': social_brand,
        'reposts': reposts,
        'date': date,
        'time': time,
        'updatetime': uptime,
    }

