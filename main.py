import sys
sys.path.append('Parsers')

import Parsers.Parse_all as parse
import Filtration.location as location
import LayoutAndSend.LayoutEmail as layout
import LayoutAndSend.SendEmail as send

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
all_news = location.location_filter(all_news)
msg = layout.layout(all_news)
send.send(msg)
