import urllib.request
import json
import httplib2
import time

def parse(word):
    all_news = []
    url = httplib2.iri2uri('https://smi2.ru/api/search?limit=100&offset=0&order=date&query={}'.format(word))
    while True:
        try:
            jsonurl = urllib.request.urlopen(url)
        except urllib.error.HTTPError as error:
            print(error)
            print('Trying again')
        else:
            break
    obj = json.load(jsonurl)
    articles = obj['articles']
    for art in articles:
        if(int(art['create_date']) < time.time() - 86400):
            continue
        news = {'title': '', 'article': '', 'link': ''}
        news['title'] = art['title_original']
        news['article'] = art['announce_original']
        news['link'] = art['share_url']
        all_news.append(news)
    return all_news
