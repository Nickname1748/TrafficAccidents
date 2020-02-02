from sklearn.feature_extraction.text import TfidfVectorizer
import pymorphy2

number = {
    'один' : '1',
    'два' : '2',
    'двое' : '2',
    'три' : '3',
    'трое' : '3',
    'четыре' : '4',
    'четверо' : '3',
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
    die = 0
    injured = 0

    for obj in check(post, TfidfVectorizer(), pymorphy2.MorphAnalyzer(), ['погибнуть', 'получить', 'жерта'], ['погиб', 'погибла']):
        die += int(obj)

    for obj in check(post, TfidfVectorizer(), pymorphy2.MorphAnalyzer(), ['пострадать', 'получить', 'жерта'], ['пострадал', 'пострадала']):
        injured += int(obj)

    print('Погибших: ' + str(die))
    print('Пострадавших: ' + str(injured))
        

def check(post, vectorizer, morph, key_words, unique_words):
    words = post.split(' ')

    quantity = []

    for word in words:
        for key_word in key_words:
            if morph.parse(word)[0].normal_form == key_word:
                for n in range(-2, 3):
                    if (word == unique_words[0]) or (word == unique_words[0]):
                        if '1' not in quantity:
                            return '1'

                    if (morph.parse(key_word)[0].tag.gender == 'masc') or (morph.parse(key_word)[0].tag.gender == 'femn'):
                        if '1' not in quantity:
                            return '1'

                    if ((words.index(word) + n) > 0) or ((words.index(word) + n) < len(words)):
                        ww = words[words.index(word) + n]
                        if (morph.parse(ww)[0].tag.POS == 'NUMR') or ('NUMB' in morph.parse(ww)[0].tag):
                            if str(ww) not in quantity:
                                if int_check(ww):
                                    quantity.append(morph.parse(ww)[0].normal_form)
                                else:
                                    quantity.append(number[morph.parse(ww)[0].normal_form])

    return quantity

#number_of_victims('Более 10 туристов пострадали в ДТП в Австралии')
#number_of_victims('Один человек погиб и 12 пострадали в ДТП в Кабардино-Балкарии')
#number_of_victims('В результате столкновения легкового автомобиля с пассажирской «Газелью» в Кабардино-Балкарии один человек погиб и ещё 12 получили травмы различной степени тяжести.')
#number_of_victims('Два человека погибли и еще двое пострадали в ДТП в Пермском крае')
#number_of_victims('Один человек погиб и 12 пострадали в ДТП в Кабардино-Балкарии')