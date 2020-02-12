from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2
import re

number = {
    'один' : '1',
    'два' : '2',
    'двое' : '2',
    'три' : '3',
    'трое' : '3',
    'четыре' : '4',
    'четверо' : '4',
    'пять' : '5',
    'пятеро' : '5',
    'шесть' : '6',
    'шестеро' : '6',
    'семь' : '7',
    'семеро' : '7',
    'восемь' : '8',
    'девять' : '9',
    'десять' : '10',
    'одиннадцать' : '11',
    'двенадцать' : '12',
    'тринадцать' : '13',
    'четырнадцать' : '14',
    'пятнадцать' : '15',
    'шестнадцать' : '16',
    'семнадцать' : '17',
    'восемнадцать' : '18',
    'девятнадцать' : '19',
    'двадцать' : '20'
}

def int_check(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def number_of_victims(post):
    dead = 0
    injured = 0

    dead = check(post, TfidfVectorizer(), pymorphy2.MorphAnalyzer(), ['погибнуть', 'жертва', 'погибший'], ['погиб', 'погибла'])

    injured = check(post, TfidfVectorizer(), pymorphy2.MorphAnalyzer(), ['пострадать', 'получить'], ['пострадал', 'пострадала'])

    return dead, injured
        
def check(post, vectorizer, morph, key_words, unique_words):
    post = re.sub(r'[^\w\s]', '', post, re.UNICODE)
    words = post.split(' ')

    for i, word in enumerate(words):
        analyzedword = morph.parse(word)
        normword = analyzedword[0].normal_form
        for key_word in key_words:
            if normword == key_word:
                for n in range(-2, 3):
                    if analyzedword[0].tag.POS == 'VERB':
                        if analyzedword[0].tag.number == 'sing':
                            if analyzedword[0].tag.gender != 'neut':
                                return 1

                    if i + n in range(len(words)):
                        ww = words[i + n]
                        if (morph.parse(ww)[0].tag.POS == 'NUMR') or ('NUMB' in morph.parse(ww)[0].tag):
                            if int_check(ww):
                                return int(morph.parse(ww)[0].normal_form)
                            else:
                                return int(number[morph.parse(ww)[0].normal_form])
    return 0

def add_info(all_news):
    for i, news in enumerate(all_news):
        all_news[i]['dead'], all_news[i]['injured'] = number_of_victims(news['title']+' '+news['article'])
    return all_news
