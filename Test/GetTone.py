import sys
sys.path.append('.')
sys.path.append('Parsers')
import time
import Parsers.Parse_all as parse
import ToneAnalysis.ToneAnalysis as ToneAnalysis

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
all_news = ToneAnalysis.analyze(all_news)
for news in all_news:
    print(news['title']+'\n'+news['article']+'\n'+str(news['tone'])+'\n\n')