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

def layout_text_part(all_news):
    text = "За {} мы собрали {}:".format(get_localized_time(), format_news_count(len(all_news)))
    for news in all_news:
        text = text + '\n\n' + news['title'] + '\n' + news['link'] + '\n' + news['article']
    return text

def layout_html_part(all_news):
    html = '''<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <h2 style="font-family: 'Roboto', sans-serif;">За прошедший день мы собрали {} о ДТП:</h2>
        <ul>
            {}
        </ul>
    </body>
    </html>'''
    news_item = '''
            <li>
                <h4 style="font-family: 'Roboto', sans-serif;">{}</h4>
                <p style="font-family: 'Roboto', sans-serif;">{}</p>
                <a style="font-family: 'Roboto', sans-serif;" href="{}">Источник</a>
            </li>'''
    all_items = []
    for news in all_news:
        all_items.append(news_item.format(news['title'], news['article'], news['link']))
    html = html.format(format_news_count(len(all_news)), '\n'.join(all_items))
    return html

def layout(all_news):
    msg = MIMEMultipart()
    msg['Subject'] = "Новости о ДТП за {}".format(get_localized_time())
    # textpart = MIMEText(layout_text_part(all_news), 'plain')
    htmlpart = MIMEText(layout_html_part(all_news), 'html')
    # msg.attach(textpart)
    msg.attach(htmlpart)
    return msg
