import sqlite3
from Parsers.Parse_all import main 

class DB:
	#---------- sqlite3 ----------#
	conn = ""
	cursor = ""
	#----------- parse -----------#
	title = ""
	article = ""
	link = ""
	#------------ END ------------#

	#-------- Создание БД --------#
	def create_db():
		conn = sqlite3.connect("traffic_accidents.db")
		cursor = conn.cursor()

		cursor.execute("""CREATE TABLE dtp (title text, article text, link text)""")
		conn.commit()
	#------------ END ------------#

	#------- Заполнение БД -------#
	@staticmethod
	def fill_db(KEY_WORDS:list):
		conn = sqlite3.connect("traffic_accidents.db")
		cursor = conn.cursor()

		a = main(KEY_WORDS)
		
		for i in a: 
			cursor.execute("""INSERT INTO dtp VALUES (?,?,?)""", (i['title'], i['article'], i['link']))
		
		conn.commit()
	#------------ END ------------#

#--------- Новая БД: ---------#
#DB.create_db()
#------------ END ------------#

#------ Ключевый слова -------#
keys = ["ДТП", "сбили пешехода", "велоспипедист"]
#------------ END ------------#

#------- Заполнение БД -------#
DB.fill_db(keys)
#------------ END ------------#
