import urllib.request
import json
import httplib2
import time

all_news = []
KEY_WORDS = ['ДТП', 'сбили%20пешехода']

class News():
	title = ""
	article = ""
	link = ""

def parse(url):
    jsonurl = urllib.request.urlopen(url)
    obj = json.load(jsonurl)
    articles = obj['articles']
    for art in articles:
        if(int(art['create_date']) < time.time() - 86400):
            continue
        news = News()
        news.title = art['title_original']
        news.article = art['announce_original']
        news.link = art['share_url']
        all_news.append(news)

for word in KEY_WORDS:
    parse(httplib2.iri2uri('https://smi2.ru/api/search?limit=100&offset=0&order=date&query={}'.format(word)))
