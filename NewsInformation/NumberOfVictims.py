from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2
import re

number = {
    'один' : '1',
    'два' : '2',
    'двое' : '2',
    'оба': '2',
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
    'двадцать' : '20',
    'двадцать один' : '21',
    'двадцать два' : '22',
    'двадцать три' : '23',
    'двадцать четыре' : '24',
    'двадцать пять' : '25',
    'двадцать шесть' : '26',
    'двадцать семь' : '27',
    'двадцать восемь' : '28',
    'двадцать девять' : '29',
    'тридцать' : '30',
    'тридцать один' : '31',
    'тридцать два' : '32',
    'тридцать три' : '33',
    'тридцать четыре' : '34',
    'тридцать пять' : '35',
    'тридцать шесть' : '36',
    'тридцать семь' : '37',
    'тридцать восемь' : '38',
    'тридцать девять' : '39',
    'сорок' : '40',
    'сорок один' : '41',
    'сорок два' : '42',
    'сорок три' : '43',
    'сорок четыре' : '44',
    'сорок пять' : '45',
    'сорок шесть' : '46',
    'сорок семь' : '47',
    'сорок восемь' : '48',
    'сорок девять' : '49',
    'пятьдесят' : '50',
    'пятьдесят один' : '51',
    'пятьдесят два' : '52',
    'пятьдесят три' : '53',
    'пятьдесят четыре' : '54',
    'пятьдесят пять' : '55',
    'пятьдесят шесть' : '56',
    'пятьдесят семь' : '57',
    'пятьдесят восемь' : '58',
    'пятьдесят девять' : '59',
    'шестьдесят' : '60',
    'шестьдесят один' : '61',
    'шестьдесят два' : '62',
    'шестьдесят три' : '63',
    'шестьдесят четыре' : '64',
    'шестьдесят пять' : '65',
    'шестьдесят шесть' : '66',
    'шестьдесят семь' : '67',
    'шестьдесят восемь' : '68',
    'шестьдесят девять' : '69',
    'семьдесят' : '70',
    'семьдесят один' : '71',
    'семьдесят два' : '72',
    'семьдесят три' : '73',
    'семьдесят четыре' : '74',
    'семьдесят пять' : '75',
    'семьдесят шесть' : '76',
    'семьдесят семь' : '77',
    'семьдесят восемь' : '78',
    'семьдесят девять' : '79',
    'восемьдесят' : '80',
    'восемьдесят один' : '81',
    'восемьдесят два' : '82',
    'восемьдесят три' : '83',
    'восемьдесят четыре' : '84',
    'восемьдесят пять' : '85',
    'восемьдесят шесть' : '86',
    'восемьдесят семь' : '87',
    'восемьдесят восемь' : '88',
    'восемьдесят девять' : '89',
    'девяносто' : '90',
    'девяносто один' : '91',
    'девяносто два' : '92',
    'девяносто три' : '93',
    'девяносто четыре' : '94',
    'девяносто пять' : '95',
    'девяносто шесть' : '96',
    'девяносто семь' : '97',
    'девяносто восемь' : '98',
    'девяносто девять' : '99',
    'сто' : '100'
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

    dead = check(post, TfidfVectorizer(), pymorphy2.MorphAnalyzer(), ['погибнуть', 'скончаться', 'жертва', 'жертвы', 'погибший'])

    injured = check(post, TfidfVectorizer(), pymorphy2.MorphAnalyzer(), ['пострадать', 'получить'])

    return dead, injured


def check(post, vectorizer, morph, key_words):
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
