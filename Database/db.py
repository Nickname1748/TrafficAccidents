import mysql.connector
import datetime

def putindb(all_news):
	db = mysql.connector.connect(
		host='localhost',
		user='backuser',
		passwd='P@ssw0rd', # Test password
		database='TrafficAccidents'
	)
	cursor = db.cursor()

	date = datetime.date.today()
	idgroup = int(date.strftime('%Y%m%d')+'01')
	idnews = int(date.strftime('%Y%m%d')+'001')
	sqlnews = 'INSERT INTO News (ID, Date, Title, Article, Link, Location, Tone, GroupID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
	sqlgroups = 'INSERT INTO Groups (ID, Date, Title) VALUES (%s, %s, %s)'
	for news in all_news:
		if type(news) == list:
			valsgroup = (idgroup, date, news[0]['title'])
			cursor.execute(sqlgroups, valsgroup)
			for item in news:
				valsitem = (idnews, date, item['title'], item['article'], item['link'], item['place'], float(item['tone']['negative']), idgroup)
				cursor.execute(sqlnews, valsitem)
				idnews += 1
			idgroup += 1
		else:
			vals = (idnews, date, news['title'], news['article'], news['link'], news['place'], float(news['tone']['negative']), -1)
			cursor.execute(sqlnews, vals)
			idnews += 1
	
	db.commit()
	cursor.close()
	db.close()
