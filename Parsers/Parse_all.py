from Parsers import ParseGoogleAlerts
from Parsers import ParseSMI2
from Parsers import ParseMailRuNews

def main(KEY_WORDS:list):
    news = []
    for i in KEY_WORDS:
        news.extend(ParseGoogleAlerts.parse(i))
        news.extend(ParseMailRuNews.parse(i))
        news.extend(ParseSMI2.parse(i))
    return news