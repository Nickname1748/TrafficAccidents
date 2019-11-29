from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import locale

def layout(all_news):
    locale.setlocale(locale.LC_ALL, '')
    msg = MIMEMultipart()
    msg['Subject'] = "Новости о ДТП за {}".format(time.strftime("%e %B %Y года", time.gmtime(time.time())))
    # Not implemented yet
    #msg['From'] = 
    #msg['To'] = 
    text = "За {} мы собрали следующие новости:".format(time.strftime("%e %B", time.gmtime(time.time())))
    for news in all_news:
        text = text + '\n\n' + news['title'] + '\n' + news['link'] + '\n' + news['article']
    textpart = MIMEText(text, 'plain')
    # TODO: HTML part
    msg.attach(textpart)
    return msg
