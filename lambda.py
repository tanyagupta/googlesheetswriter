import requests
import re
import time
import inspect
import os
#from constants import ACTIVE_ENDPOINT as ENDPOINT
import json
from bs4 import BeautifulSoup


from html import unescape

from pygooglenews import GoogleNews

ENDPOINT = "https://script.google.com/macros/s/AKfycbzV5efRKkHa4W9AM4hEmr7pUlC0CK1bsc3sPdKCsO3vInoQVKY/exec"
limit_for_free_news = 15

import json

def lambda_handler(event, context):
   return main()


def get_news(news_type):

    gn = GoogleNews()
    if news_type == "free":
        top = gn.top_news()

    if news_type == "top":
        top = gn.top_news()
        process_news(top,"free")
    if news_type == "business":
        business = gn.topic_headlines('BUSINESS', proxies=None, scraping_bee = None)
        process_news(business,"business")
    if news_type == "world":
        world = gn.topic_headlines('WORLD', proxies=None, scraping_bee = None)
        process_news(world,"world")
    if news_type == "nation":
        nation = gn.topic_headlines('NATION', proxies=None, scraping_bee = None)
        process_news(nation,"nation")
    if news_type == "technology":
        technology = gn.topic_headlines('TECHNOLOGY', proxies=None, scraping_bee = None)
        process_news(technology,"technology")
    if news_type == "sports":
        sports = gn.topic_headlines('SPORTS', proxies=None, scraping_bee = None)
        process_news(sports,"sports")
    if news_type == "health":
        health = gn.topic_headlines('HEALTH', proxies=None, scraping_bee = None)
        process_news(health,"health")
    if news_type == "entertainment":
        entertainment = gn.topic_headlines('ENTERTAINMENT', proxies=None, scraping_bee = None)
        process_news(entertainment,"entertainment")
    if news_type == "science":
        science = gn.topic_headlines('SCIENCE', proxies=None, scraping_bee = None)
        process_news(science,"science")



def process_news(news_cat,news_type):


    entries = news_cat["entries"]
    if news_type == "free":
        entries = entries[:limit_for_free_news]

    if len(entries) > 35:
        entries = entries[:35]




    processed_news = []
    for k in entries:

        summary = k["summary"]
        #summary = BeautifulSoup(k["summary"]).get_text()
        summary = BeautifulSoup(k["summary"],features="html.parser").get_text().replace('\xa0', ' ')
        #summary = BeautifulSoup(k["summary"]).get_text(strip=True)
        title = k["title"]
        source_name = k["source"]["title"]
        source_url = k["source"]["href"]
        link = k["link"]
        published = k["published"]
        r = requests.head(link, allow_redirects=True)
        time.sleep(.1)
        original_news_link = r.url
        is_image = get_image(original_news_link)
        if len(is_image) > 0:
            image_url = is_image[0]
        else:
            image_url=""
        processed_news.append([title,summary,source_name,original_news_link,source_url,link,published,image_url])

    new_array=clean_test_in_array(processed_news)

    num_rows = len(processed_news)
    num_cols = len(processed_news[0])
    notation = determine_notation(num_rows,num_cols)
    a1_notation = news_type+"!"+notation
    #add_data(a="b")
    add_data(a={"do":"add_data", "params" : {"ss_id":"1Bc6FUWBXUpZB_zAOpsg_EJN4NGKgR2gOGP-NjgIOKvs","a1Notation":a1_notation,"values":processed_news}})
    a1_notation = "all"+"!"+notation
    add_data(a={"do":"add_data", "params" : {"ss_id":"1Bc6FUWBXUpZB_zAOpsg_EJN4NGKgR2gOGP-NjgIOKvs","a1Notation":a1_notation,"values":processed_news}})


def get_image(url):

    getURL = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    time.sleep(.1)
    soup = BeautifulSoup(getURL.text, 'html.parser')


    images = soup.find_all('img')
    resolvedURLs = []
    if len(images)>0:


        for image in images:
            src = image.get('src')
            resolvedURLs.append(requests.compat.urljoin(url, src))


    return resolvedURLs



def determine_notation(num_rows,num_cols):
    #rows then columns
    lookup = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
    a1_elem1 = "A1"
    a1_elem2 = lookup.get(num_cols)

    return a1_elem1+":"+str(a1_elem2)+str(num_rows)

# WORLD NATION BUSINESS TECHNOLOGY ENTERTAINMENT SCIENCE SPORTS HEALTH

def add_data (**kwargs):
    """
    Make a POST request to a GAS server.
    : param str ss_id: The ID of the Google Spreadsheet where the data will be added to
    : param str a1: Data to be writeen in a1 notation. Must include the sheet_name
    : param values: A two d array of values, must match the dimension of the data range give in a1Notation

    : https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#info-field-lists

    """
    my_payload=kwargs["a"]

    #my_payload = {"do":"add_data", "params" : {"ss_id":"1Bc6FUWBXUpZB_zAOpsg_EJN4NGKgR2gOGP-NjgIOKvs","a1Notation":"A1:D1","values":[["boo", "a", "d", "e"]]}}

    #{a1Notation=A1:D1, ss_id=12Tv6J_B0Y1llqlQFJh5Wr0jfxEiB40avjI5sQpPOCwg, values=[[blah, a, d, e]]}
    """
    print (my_payload["params"]["ss_id"], my_payload["params"]["a1Notation"])
    """

    #ENDPOINT="https://docs.google.com/spreadsheets/d/1Bc6FUWBXUpZB_zAOpsg_EJN4NGKgR2gOGP-NjgIOKvs/edit?gid=423524239"
    print(ENDPOINT)
    print(my_payload)
    r = requests.post(ENDPOINT, data = json.dumps(my_payload))
    return  r.text


def main():
    categories = ["free","top","world","nation","business","technology","entertainment","science","sports","health"]
#    categories = ["top","world","nation","business","technology","entertainment","sports","health"]
    for item in categories:
        get_news(item)
        time.sleep(.1)


if __name__ == "__main__":
    main()
