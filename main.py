import sys
sys.path.append('Parsers')

import Parsers.Parse_all as parse
import LayoutAndSend.LayoutEmail as layout

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
msg = layout.layout(all_news)

