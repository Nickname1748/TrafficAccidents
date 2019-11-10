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
	page = website.findAll('li', 'result')
	for n in range(len(page)):
		news = News()
		if (page[n].find('img') != None):
			news.title = page[n].find('h4').text
		else:
			news.title= page[n].find('a').text
		news.article = page[n].find('span').text
		news.link = page[n].find('a', 'result_title_link')['href']
		all_news.append(news)		

parse('https://www.google.ru/alerts/preview?params=[null,[null,null,null,[null,"\u0434\u0442\u043f","ru",[null,"ru","RU"],null,null,null,0,1],null,3,[[null,1,"user@example.com",[null,null,10],2,"ru-RU",null,null,null,null,null,"0",null,null,"AB2Xq4hcilCERh73EFWJVHXx-io2lhh1EhC8UD8"]]],0]')
