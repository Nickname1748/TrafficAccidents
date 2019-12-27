from natasha import LocationExtractor
import requests
import json

def delete_abroad(news):
    format_news = []
    for i in range(len(news)):
        print(i)
        if (news[i]['country_code'] == "") or (news[i]['country_code'] == "RU"):
            format_news.append(news[i])
    return format_news

def get_full_address_and_country_code(news):
    API_KEY = "" #Yandex GeoCoder API key required
    URL = "https://geocode-maps.yandex.ru/1.x?geocode={}&apikey={}&format=json"
    for i in range(len(news)):
        if news[i]['place'] != '':
            a = requests.get(URL.format(news[i]['place'], API_KEY))
            json_data = json.loads(a.text)
            if len(json_data['response']['GeoObjectCollection']['featureMember']) != 0:
                place = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                try:
                    country_code = json_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['country_code']
                except KeyError:
                    country_code = ""
                news[i]['place'] = place
                news[i].update({'country_code':country_code})
            else:
                news[i].update({'country_code': ""})
        else:
            news[i].update({'country_code':''})
    print(news[17])
    return news
def add_place(news):
    extractor = LocationExtractor()
    for i in range(len(news)):
        matches = extractor(news[i]['article'])
        if len(matches.as_json) == 0:
            matches = extractor(news[i]['title'])
            if (len(matches.as_json) == 0):
                news[i].update({'place':''})
            else:
                places = []
                for k in range(len(matches.as_json)):
                    places.append(matches.as_json[k]['fact']['name'])
                for j in range(len(places)):
                    places[j] = places[j].title()
                news[i].update({'place':','.join(places)})
        else:
            places = []
            for k in range(len(matches.as_json)):
                places.append(matches.as_json[k]['fact']['name'])
            for j in range(len(places)):
                places[j] = places[j].title()
            news[i].update({'place':','.join(places)})
    return news

def location_filter(news):
    news = add_place(news)
    news = get_full_address_and_country_code(news)
    news = delete_abroad(news)
    return news
