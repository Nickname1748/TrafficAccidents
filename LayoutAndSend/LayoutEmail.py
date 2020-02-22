from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import locale
import io

# Tested to work on Linux. For other platforms not guaranteed to work.
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

def get_localized_time():
    a = time.strftime("%e %B %Y года", time.gmtime(time.time()))
    return a

def format_news_count(n):
    d = n % 10
    if d == 1 and n % 100 != 11:
        return "{} новость".format(n)
    elif d > 1 and d < 5 and n / 10 % 10 != 1:
        return "{} новости".format(n)
    else:
        return "{} новостей".format(n)

def format_victims_count(dead, injured):
    deadtext = ''
    injtext = ''
    if dead > 0:
        deadtext = 'Погибших: '+str(dead)
    if injured > 0:
        injtext = 'Пострадавших: '+str(injured)
    
    if deadtext != '' and injtext != '':
        return deadtext + ' ' + injtext
    else:
        return deadtext + injtext

def layout_text_part(all_news):
    text = "За {} мы собрали {}:".format(get_localized_time(), format_news_count(len(all_news)))
    for news in all_news:
        text = text + '\n\n' + news['tone']['negative'] + '\n' + news['title'] + '\n' + news['place'] + '\n' + news['link'] + '\n' + news['article']
    return text

def layout_html_part(all_news):
    all_news = all_news[:15] # Show only 15 news, rest news at site
    template = open('html/emailtemplate.html', 'r').read()
    newsgrouptemplate = open('html/emailnewsgrouptemplate.html', 'r').read()
    newsgroupitemtemplate = open('html/emailnewsgroupitemtemplate.html', 'r').read()
    newsitemtemplate = open('html/emailnewsitemtemplate.html', 'r').read()
    groups = []
    newsitems = []
    for news in all_news:
        if type(news) == list:
            groupitems = []
            for item in news:
                groupitems.append(newsgroupitemtemplate.format(item['tone']['negative'], format_victims_count(item['dead'], item['injured']), item['title'], item['link'], item['article']))
            groups.append(newsgrouptemplate.format(news[0]['place'], news[0]['title'], '\n'.join(groupitems)))
        else:
            newsitems.append(newsitemtemplate.format(news['place'], news['tone']['negative'], format_victims_count(news['dead'], news['injured']), news['title'], news['link'], news['article']))
    groups.extend(newsitems)
    html = template.format(get_localized_time(), format_news_count(len(all_news)), '\n'.join(groups))
    return html

def layout(all_news):
    msg = MIMEMultipart()
    msg['Subject'] = "Новости о ДТП за {}".format(get_localized_time())
    # textpart = MIMEText(layout_text_part(all_news), 'plain')
    htmlpart = MIMEText(layout_html_part(all_news), 'html')
    # msg.attach(textpart)
    msg.attach(htmlpart)
    return msg
