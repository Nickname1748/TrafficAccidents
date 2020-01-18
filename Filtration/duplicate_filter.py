import nltk # Natural Language Toolkit
nltk.download('stopwords')
from pymorphy2 import MorphAnalyzer # Morphological analyzer for Russian language
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer # Machine learning
from sklearn.metrics.pairwise import cosine_distances

def lemmatization(list_of_strings):
    morph = MorphAnalyzer()
    for i in range(len(list_of_strings)):
        list_of_strings[i] = morph.parse(list_of_strings[i])[0].normal_form
    return list_of_strings

get_list_of_strings = lambda all_news: [news['article'] for news in all_news]

def clear_corpus(list_of_strings):
    StopWords = stopwords.words('russian')
    for i in range(len(list_of_strings)):
        for k in range(len(StopWords)):
            list_of_strings[i] = re.sub(StopWords[k], "", list_of_strings[i])
    return list_of_strings

def get_vector(list_of_strings):
    tfidf_vectorizer = TfidfVectorizer()
    vectors = tfidf_vectorizer.fit_transform(list_of_strings)
    return vectors

def compare_cosine_distances(vectors):
    result = cosine_distances(vectors)
    return result

def find_similar(distances):
    sets = []
    setid = [-1]*len(distances) # Every item is not a member of any set
    for i in range(len(distances)):
        for k in range(len(distances[i])):
            if k != i:
                if distances[i][k] < 0.6: #THIS NUMBER SHOULD BE TESTED
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
    sets.sort(key=lambda s: len(s))
    return sets

def main_filter(news):
    list_of_strings = get_list_of_strings(news)
    list_of_strings = clear_corpus(list_of_strings) # Remove unneeded words
    list_of_strings = lemmatization(list_of_strings)
    vectors = get_vector(list_of_strings)
    distances = compare_cosine_distances(vectors)
    sets = find_similar(distances)
    finalnews = [] # Put all news to groups
    for s in sets:
        newsgroup = []
        for i in s:
            newsgroup.append(news.pop(i))
        finalnews.append(newsgroup)
    finalnews.extend(news) # Add remained news without groups
    return finalnews
