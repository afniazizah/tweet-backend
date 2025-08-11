from app import app, TWEETS_DATA_PATH
import uuid
import pandas as pd

from googletrans import Translator
translator = Translator()

def translate_tweet(tweet):
    try:
        translated = translator.translate(tweet, dest='id')
        return translated.text
    except Exception as e:
        return str(e)

def translate_all(file):
    data = pd.read_csv(file)
    data = pd.DataFrame(data[['full_text']])
    data['data_translate'] = data['full_text'].apply(translate_tweet)
    data['full_text'] = data['data_translate']
    filename = str(uuid.uuid4()) + '.csv'
    data.to_csv(TWEETS_DATA_PATH + '/' + filename, index=False)
    return filename
