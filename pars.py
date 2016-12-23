# -*- coding: utf-8 -*-
__author__ = 'MA573RWARR10R'
import sqlite3
import urllib3
from info import *
from page import *
import requests
import json
from bs4 import BeautifulSoup


def make_pretty_url(url):
    if re.match("^/", url):
        return base_url[:-1] + url

    return url


def short_article_url(url):
    l = re.findall("([0-9]+\.html$)", url)
    if len(l) == 1:
        return base_url + l[0]

    return url


def get_list_json_data(page, site_id, resource_id):
    return get_content_from_url(
        "https://www.paperscrap/core/load_more_posts/data.js?pn={page}&resource_id={resource_id}&site_id={site_id}".format(
            page=page, resource_id=resource_id, site_id=site_id))


def get_urls_from_long_list(url, existing):
    art_by_cat = get_content_from_url(url)

    l = re.findall("site_id=(.*)&resource_id=(.*)'", art_by_cat)
    if len(l) == 0:
        print(("\tWarning! Can't find resource id and site id at url %s" % url))
        return []

    page_id = 0
    art_urls = []
    while True:
        raw_data = get_list_json_data(page_id, l[0][0], l[0][1])
        json_data = json.loads(raw_data)

        print("Page: {0}".format(page_id))
        if len(json_data["posts_by_source"]["frontpage"]) == 0:
            break

        for pbs in json_data["posts_by_source"]:
            for key in json_data["posts_by_source"][pbs]:
                if isinstance(key, dict):
                    url = base_url + str(key["_id"]) + ".html"
                    if url not in existing:
                        print("New found: {0}".format(url))
                        art_urls.append(url)
                    #save_one(url, 'papermag_urls.txt')

        page_id += 1

    if len(art_urls) == 0:
        print("Can't get urls from %s" % url)
        
    return art_urls


def get_content_from_url(url_):
    req = urllib3.Request(url_)
    res = urllib3.urlopen(req)

    return res.read()


def is_article(current_url):
    return re.match(r"paperscrap\/[\w\-]{10}\.html", current_url)


def has_base_domain(url):  # todo check!!!
    return re.match("(http|https)\:\/\/(www\.|)%s" % domain_name, url)


def get_possible_urls(page_data):
    all = []

    soup = BeautifulSoup(page_data, "lxml")
    for tag_a in soup.find_all("a"):
        if "href" not in tag_a.attrs:
            continue

        url = make_pretty_url(tag_a.attrs["href"])

        if has_base_domain(url):
            all.append(url)

    return all


def save_one(url, fname):
    with open(fname, 'a') as f:
        f.write(url + "\n")


def get_urls_from_doc(name):
    urls = set()

    with open(name, 'r') as f:
        for line in f.readlines():
            urls.add(line[:-1])

    return urls


def start():
    article_urls = []
    parsed_urls = get_urls_from_doc('papermag_urls.txt')
    url_queue_to_parse = set()

    url_queue_to_parse.add(base_url)

    while len(url_queue_to_parse) > 0:
        current_url = url_queue_to_parse.pop()

        # if is_article(current_url):
        #     article_urls.append(current_url)

        if current_url not in parsed_urls:
            parsed_urls.add(current_url)
            save_one(current_url, 'papermag_urls.txt')
        else:
            break

        page_data = get_content_from_url(current_url)

        next_urls = get_possible_urls(page_data)
        next_urls += get_urls_from_long_list(current_url, parsed_urls)

        if len(next_urls) != 0:
            for nu in next_urls:
                next_ok = short_article_url(nu)

                parsed_urls.add(next_ok)
                save_one(next_ok, 'papermag_urls.txt')

                url_queue_to_parse.add(next_ok)

    print("SUCCESS!")


if __name__ == "__main__":
    pass
    #start()  # conn, table_name)
