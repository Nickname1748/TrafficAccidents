import nltk
nltk.download('stopwords')
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
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
    f = []
    pares = []
    result = []
    for i in distances:
        f.append(list(i))
    for i in range(len(distances)):
        for k in range(len(distances[i])):
            if k != i:
                if distances[i][k] < 0.6: #THIS NUMBER SHOULD BE TESTED
                    pares.append(frozenset([i,k]))
    for i in range(len(pares)):
        if pares[i] not in result:
            result.append(pares[i])
    return result

def main_filter(news):
    list_of_strings = get_list_of_strings(news)
    list_of_strings = clear_corpus(list_of_strings)
    vectors = get_vector(list_of_strings)
    distances = compare_cosine_distances(vectors)
    result = find_similar(distances)
    return result