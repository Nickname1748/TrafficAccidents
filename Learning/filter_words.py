import sys
sys.path.append('.')
sys.path.append('Parsers')
import Parsers.Parse_all as parse
import Filtration.duplicate_filter as filter

KEY_WORDS = ['дтп', 'пешеход', 'сбили%20пешехода', 'на%20пешеходном%20переходе', 'на%20зебре']

all_news = parse.main(KEY_WORDS)

news = filter.remove_same(all_news) # Remove exact same news
list_of_strings = filter.get_list_of_strings(all_news)
list_of_strings = filter.clear_corpus(list_of_strings) # Remove unneeded words
list_of_strings = filter.lemmatization(list_of_strings)

good_words = set()
bad_words = set()
for i in range(len(all_news)):
    print(all_news[i]['title'])
    print(all_news[i]['article'])
    words = set(list_of_strings[i].split())
    rel = input('Is that good? (y/n) ')
    if rel == 'y':
        good_words = good_words.union(words)
    else:
        bad_words = bad_words.union(words)

final_words = bad_words.difference(good_words)

print(bad_words)
print(good_words)
print(final_words)