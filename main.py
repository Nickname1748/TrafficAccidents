import sys
sys.path.append('Parsers')

from email.mime.multipart import MIMEMultipart

import Parsers.Parse_all as parse
import Filtration.location as location
import Filtration.duplicate_filter as duplicate_filter
import LayoutAndSend.LayoutEmail as layout
import LayoutAndSend.SendEmail as send

args = sys.argv

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
all_news = location.location_filter(all_news)
all_news = duplicate_filter.main_filter(all_news)
if '--nosend' not in args:
    msg = layout.layout(all_news)
    send.send(msg)
else:
    if '--html' not in args:
        output = layout.layout_text_part(all_news)
    else:
        output = layout.layout_html_part(all_news)
    if '--file' not in args:
        print(output)
    else:
        if '--html' in args:
            filename = 'output.html'
        else:
            filename = 'output.txt'
        f = open(filename, 'w')
        f.write(output)
