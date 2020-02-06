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

	sql = "INSERT INTO News (Date, Title, Article, Link, Location) VALUES (%s, %s, %s, %s, %s)"
	date = datetime.date.today()
	for news in all_news:
		if type(news) == list:
			for item in news:
				vals = (date, item['title'][:250], item['article'][:250], item['link'], item['place'])
				cursor.execute(sql, vals)
		else:
			vals = (date, news['title'], news['article'], news['link'], news['place'])
			cursor.execute(sql, vals)
	
	db.commit()
	cursor.close()
	db.close()
