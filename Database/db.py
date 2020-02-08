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

	sql = "INSERT INTO News (Date, Title, Article, Link, Location) VALUES (%s, %s, %s, %s, %s, %s)"
	date = datetime.date.today()
	for news in all_news:
		if type(news) == list:
			for item in news:
				vals = (date, item['title'], item['article'], item['link'], item['place'], item['tone']['negative'])
				cursor.execute(sql, vals)
		else:
			vals = (date, news['title'], news['article'], news['link'], news['place'], news['tone']['negative'])
			cursor.execute(sql, vals)
	
	db.commit()
	cursor.close()
	db.close()
