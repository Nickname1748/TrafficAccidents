import sys
sys.path.append('.')
sys.path.append('Parsers')
import time
import Parsers.Parse_all as parse

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
f = open(time.strftime('news-%Y-%m-%d', time.gmtime(time.time())), 'w')
f.write(time.strftime('Generated at %Y-%m-%dT%H:%M:%S\n', time.gmtime(time.time())))
for news in all_news:
    f.write('\n' + news['title'] + '\n' + news['link'] + '\n' + news['article'] + '\n')
f.close()
