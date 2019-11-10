import urllib.request
import json

all_news = []

class News():
	title = ""
	article = ""
	link = ""

def parse(url):
    jsonurl = urllib.request.urlopen(url)
    obj = json.load(jsonurl)
    articles = obj["articles"]
    for art in articles:
        news = News()
        news.title = art["title_original"]
        news.article = art["announce_original"]
        news.link = art["share_url"]
        all_news.append(news)

parse('https://smi2.ru/api/search?limit=30&offset=0&order=date&query=%D0%BF%D0%B5%D1%88%D0%B5%D1%85%D0%BE%D0%B4')