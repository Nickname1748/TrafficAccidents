import requests
from bs4 import BeautifulSoup

all_news = []
KEY_WORDS = ['пешеход', 'сбили пешехода']

class News():
	title = ""
	article = ""
	link = ""

def parse(lxml): 
	request = requests.get(lxml)
	website = BeautifulSoup(request.text, 'html.parser')
	page = website.findAll('div', 'newsitem')
	for n in range(len(page)):
		if(page[n].find('span', 'newsitem__title-inner') == None or page[n].find('div', 'newsitem_itsinterest') != None):
			continue
		news = News()
		news.title = page[n].find('span', 'newsitem__title-inner').text
		news.article = page[n].find('span', 'newsitem__text').text
		news.link = 'https://news.mail.ru' + page[n].find('a', 'newsitem__title link-holder')['href']
		all_news.append(news)		

for i in range(len(KEY_WORDS)):
	parse('https://news.mail.ru/search/?usid=90&q={}'.format(KEY_WORDS[i]))
print(all_news)