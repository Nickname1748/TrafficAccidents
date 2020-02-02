from natasha import LocationExtractor
import requests
import json

def ifCrimea(json_data):
    flag = False
    a = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components']
    for i in a:
        if i['name'] == 'Республика Крым':
            flag = True
    return flag

def delete_abroad(news):
    format_news = []
    for i in range(len(news)):
        if (news[i]['country_code'] == "") or (news[i]['country_code'] == "RU"):
            format_news.append(news[i])
    return format_news

def get_full_address_and_country_code(all_news):
    apikeyfile = open('geocoderapikey.txt')
    API_KEY = apikeyfile.read().strip('\n')
    URL = "https://geocode-maps.yandex.ru/1.x?geocode={}&apikey={}&format=json"
    for i in range(len(all_news)):
        flag = False
        if all_news[i]['place'] != '':
            a = requests.get(URL.format(all_news[i]['place'], API_KEY))
            json_data = json.loads(a.text)
            if len(json_data['response']['GeoObjectCollection']['featureMember']) != 0:
                place = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                try:
                    if ifCrimea(json_data):
                        country_code = 'UA'
                        flag = True
                    if not(flag):
                        country_code = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['country_code']
                except KeyError:
                    country_code = ""
                all_news[i]['place'] = place
                all_news[i].update({'country_code':country_code})
            else:
                all_news[i].update({'country_code': ""})
        else:
            all_news[i].update({'country_code':''})
    return all_news

def add_place(all_news):
    extractor = LocationExtractor()
    for i in range(len(all_news)):
        text = ' '.join([all_news[i]['title'], all_news[i]['article']])
        matches = extractor(text)
        all_news[i].update({'place':''})
        if len(matches.as_json) > 0:
            places = []
            for match in matches.as_json:
                places.append(match['fact']['name'])
            for j in range(len(places)):
                places[j] = places[j].title()
            all_news[i].update({'place':','.join(places)})
    return all_news

def location_order(news):
    f = open('linux_cities.txt', 'r')
    new_array = []
    locations = [i['location'] for i in news]
    for i in f:
        k = locations.find(i)
        while k != -1:
            new_array.append(news.pop(k))
    new_array.extend(news)
    return new_array

def location_filter(news):
    news = add_place(news)
    news = get_full_address_and_country_code(news)
    news = delete_abroad(news)
    news = location_filter(news)
    return news
