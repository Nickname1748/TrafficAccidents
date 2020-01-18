import sys
sys.path.append('.')
sys.path.append('Parsers')
import Parsers.Parse_all as parse
import Filtration.location as location
import Filtration.duplicate_filter as duplicate_filter

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода']

all_news = parse.main(KEY_WORDS)
all_news = location.location_filter(all_news)
result = duplicate_filter.main_filter(all_news)
print(result)
