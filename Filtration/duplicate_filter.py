import nltk # Natural Language Toolkit
nltk.download('stopwords')
from pymorphy2 import MorphAnalyzer # Morphological analyzer for Russian language
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer # Machine learning
from sklearn.metrics.pairwise import cosine_distances

def remove_same(news):
    news.sort(key=lambda n: n['title'])
    i = 0
    while i < len(news) - 1:
        if news[i]['title'] == news[i+1]['title']:
            del news[i+1]
            continue
        else:
            i = i + 1
    return news

def lemmatization(list_of_strings):
    morph = MorphAnalyzer()
    for i in range(len(list_of_strings)):
        words = list_of_strings[i].split()
        for k in range(len(words)):
            words[k] = morph.parse(words[k])[0].normal_form
        list_of_strings[i] = ' '.join(words)
    return list_of_strings

get_list_of_strings = lambda all_news: [news['title']+' '+news['article'] for news in all_news]

def clear_corpus(list_of_strings):
    StopWords = stopwords.words('russian')
    for i in range(len(list_of_strings)):
        list_of_strings[i] = re.sub(r'[^\w\s]', '', list_of_strings[i], re.UNICODE)
        words = list_of_strings[i].split()
        words = list(filter(lambda word: word.lower() not in StopWords, words))
        list_of_strings[i] = ' '.join(words)
    return list_of_strings

def get_vector(list_of_strings):
    tfidf_vectorizer = TfidfVectorizer()
    vectors = tfidf_vectorizer.fit_transform(list_of_strings)
    return vectors

def compare_cosine_distances(vectors):
    result = cosine_distances(vectors)
    return result

def find_similar(distances):
    distsformed = []
    for i in range(len(distances)):
        for k in range(i+1, len(distances[i])):
            distsformed.append([distances[i][k], i, k])
    distsformed.sort(key=lambda d: d[0])
    distsformed = list(filter(lambda d: d[0] < 0.6, distsformed)) #THIS NUMBER SHOULD BE TESTED
    sets = []
    setid = [-1]*len(distances) # Every item is not a member of any set
    for dist in distsformed:
        i = dist[1]
        k = dist[2]
        if setid[i] != -1:
            if setid[k] == -1:
                sets[setid[i]].add(k)
                setid[k] = setid[i]
        elif setid[k] != -1:
            if setid[i] == -1:
                sets[setid[k]].add(i)
                setid[i] = setid[k]
        else:
            setid[i] = len(sets)
            setid[k] = len(sets)
            sets.append(set([i,k]))
    sets.sort(key=lambda s: len(s), reverse=True)
    return sets

def is_relevant(newstopic):
    # IRRELEVANT_WORDS = ['трасса'] # All in normal form
    irrelevantwordsfile = open('irrelevantwords.txt', 'r')
    IRRELEVANT_WORDS = [line.rstrip('\n') for line in irrelevantwordsfile]
    morph = MorphAnalyzer()
    words = set()
    if type(newstopic) == list:
        for item in newstopic:
            itemwords = (item['title']+' '+item['article']).split()
            for i in range(len(itemwords)):
                itemwords[i] = morph.parse(itemwords[i])[0].normal_form
            words = words.union(set(itemwords))
    else:
        itemwords = (newstopic['title']+' '+newstopic['article']).split()
        for i in range(len(itemwords)):
            itemwords[i] = morph.parse(itemwords[i])[0].normal_form
        words = set(itemwords)
    for word in IRRELEVANT_WORDS:
        if word in words:
            return False
    return True

def main_filter(news):
    news = remove_same(news) # Remove exact same news
    list_of_strings = get_list_of_strings(news)
    list_of_strings = clear_corpus(list_of_strings) # Remove unneeded words
    list_of_strings = lemmatization(list_of_strings)
    vectors = get_vector(list_of_strings)
    distances = compare_cosine_distances(vectors)
    sets = find_similar(distances)
    finalnews = [] # Put all news to groups
    grouped = set()
    for s in sets:
        newsgroup = []
        for i in s:
            newsgroup.append(news[i])
            grouped.add(i)
        finalnews.append(newsgroup)
    for i in range(len(news)):
        if i not in grouped:
            finalnews.append(news[i]) # Add remained news without groups
    finalnews = list(filter(is_relevant, finalnews))
    return finalnews
