import requests
from bs4 import BeautifulSoup
import datetime
import iso8601

all_news = []
KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

def parse(url): 
	request = requests.get(url)
	website = BeautifulSoup(request.text, 'html.parser')
	page = website.findAll('div', 'newsitem')
	for n in range(len(page)):
		if(page[n].find('span', 'newsitem__title-inner') == None or page[n].find('div', 'newsitem_itsinterest') != None or page[n].find('span', 'newsitem__param') == None):
			continue
		arttime = iso8601.parse_date(page[n].find('span', 'newsitem__param')['datetime'])
		if((datetime.datetime.utcnow().astimezone(tz=datetime.timezone.utc) - arttime) > datetime.timedelta(days=1)):
			continue
		news = {'title': '', 'article': '', 'link': ''}
		news['title'] = page[n].find('span', 'newsitem__title-inner').text
		news['article'] = page[n].find('span', 'newsitem__text').text
		news['link'] = 'https://news.mail.ru' + page[n].find('a', 'link-holder')['href']
		all_news.append(news)		

for word in KEY_WORDS:
	parse('https://news.mail.ru/search/?usid=90&q={}'.format(word))
