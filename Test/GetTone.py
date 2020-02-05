import sys
sys.path.append('.')
sys.path.append('Parsers')
import time
import Parsers.Parse_all as parse
import ToneAnalysis.ToneAnalysis as ToneAnalysis

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
all_news = ToneAnalysis.analyze(all_news)
all_news.sort(key=lambda news: news['tone']['negative'])
print("{:>8} {:>8} {:>8} {}".format('Positive', 'Neutral', 'Negative', 'Article'))
for news in all_news:
    # print(news['title']+'\n'+news['article']+'\n'+str(news['tone'])+'\n\n')
    print("{:.6f} {:.6f} {:.6f} {}".format(news['tone']['positive'], news['tone']['neutral'], news['tone']['negative'], news['title']))