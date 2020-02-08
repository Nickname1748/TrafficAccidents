from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

def analyze(all_news):
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)

    texts = [news['title']+' '+news['article'] for news in all_news]
    results = model.predict(texts)
    for i in range(len(all_news)):
        all_news[i]['tone'] = results[i]
    return all_news