import sys
sys.path.append('Parsers')

from email.mime.multipart import MIMEMultipart

import Parsers.Parse_all as parse
import Filtration.location as location
import Filtration.duplicate_filter as duplicate_filter
import Database.db as db
import LayoutAndSend.LayoutEmail as layout
import LayoutAndSend.SendEmail as send

args = sys.argv

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
all_news = location.location_filter(all_news)
all_news = duplicate_filter.main_filter(all_news)
if "--nosend" not in args and "--db" not in args:
    msg = layout.layout(all_news)
    send.send(msg)
elif "--db" in args:
    db.putindb(all_news)
else:
    print(layout.layout_text_part(all_news))
