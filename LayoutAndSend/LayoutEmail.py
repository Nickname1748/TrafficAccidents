from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
import locale
import io

PASSWORD = ''

locale.setlocale(locale.LC_ALL, '')

def return_right_date_form():
    a = time.strftime("%e %B %Y года", time.gmtime(time.time()))
    a = a.split(' ')
    month_num = int(time.strftime('%m', time.gmtime(time.time())))
    if (month_num != 3) and (month_num != 8):
        a[2] = a[2].replace('ь', 'я')
    else:
        a[2] = a[2] = a[2] + 'а'
    a = " ".join(a)
    return a

def layout(all_news):
    msg = MIMEMultipart()
    msg['Subject'] = "Новости о ДТП за {}".format(return_right_date_form())
    msg['From'] = 'nickname.project@gmail.com'
    msg['To'] = 'solovyov-sasha@mail.ru'
    text = "За {} мы собрали следующие новости:".format(return_right_date_form())
    for news in all_news:
        text = text + '\n\n' + news['title'] + '\n' + news['link'] + '\n' + news['article']
    textpart = MIMEText(text, 'plain')
    htmlpart = MIMEText(make_html(all_news),'html')
    msg.attach(htmlpart)
    #msg.attach(textpart)
    fromaddr = 'nickname.project@gmail.com'
    toaddr = 'solovyov-sasha@mail.ru'
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.login('nickname.project@gmail.com', PASSWORD)
    msg_full = msg.as_string()
    server.sendmail(fromaddr, toaddr, msg_full)
    server.quit()
    return msg

def make_html(news):
    if len(news) % 10 == 1:
        template = '''<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <h2 style="font-family: 'Roboto', sans-serif;">За прошедший день была собрана {} новость о ДТП:</h2>
        {}
    </body>
    </html>'''
    elif (len(news) % 10 == 2) or (len(news) % 10 == 3) or (len(news) % 10 == 4):
        template = '''<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <h2 style="font-family: 'Roboto', sans-serif;">За прошедший день были собраны {} новости о ДТП:</h2>
        {}
    </body>
    </html>'''
    else:
        template = '''<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <h2 style="font-family: 'Roboto', sans-serif;">За прошедший день было собрано {} новостей о ДТП:</h2>
        {}
    </body>
    </html>'''
    other_template = '''
    <ul>
        <li>
            <h4 style="font-family: 'Roboto', sans-serif;">{}</h4>
            <p style="font-family: 'Roboto', sans-serif;">{}</p>
            <a style="font-family: 'Roboto', sans-serif;" href="{}">Источник</a>
        </li>
    </ul>'''
    templates = []
    for i in news:
        templates.append(other_template.format(i['title'], i['article'], i['link']))
    template = template.format(len(news),'\n'.join(templates))
    #with io.open('example.html', 'w', encoding='utf-8') as f:
    #    f.write(template)
    return template
