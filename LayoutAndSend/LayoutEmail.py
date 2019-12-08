from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
import locale
import io

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

def make_html(news):
    template = '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
    <h2 style="font-family: 'Roboto', sans-serif; margin-left: 25%;">За прошедший день было собрано {} новостей о ДТП:</h2>
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