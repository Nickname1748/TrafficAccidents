import requests
from bs4 import BeautifulSoup

all_news = []

class News():
	title = ""
	article = ""
	link = ""

def parse(lxml): 
	request = requests.get(lxml)
	website = BeautifulSoup(request.text, 'html.parser')
	page = website.findAll('div', 'newsitem')
	for n in range(len(page)):
        if(page[n].find('div', 'newsitem_itsinterest') != None):
            continue
		news = News()
		news.title = page[n].find('span', 'newsitem__title-inner').text
		news.article = page[n].find('span', 'newsitem__text').text
		news.link = page[n].find('a', 'newsitem__title link-holder')['href']
		all_news.append(news)		

parse('https://news.mail.ru/search/?usid=90&q=%D0%BF%D0%B5%D1%88%D0%B5%D1%85%D0%BE%D0%B4')
print(all_news)