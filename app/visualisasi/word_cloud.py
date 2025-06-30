import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from app import IMAGE_PATH
import datetime
import uuid

def word_cloud_tweet(data):
    text = ' '.join(data['stemming'].astype(str).tolist())

    stopwords = set(STOPWORDS)
    stopwords.update(['https', 'co', 'RT', '...', 'amp', 'lu', 'deh', 'ya', 'gue', 'kak', 'tan'])

    wc = WordCloud(background_color='white', max_words=1000, stopwords=stopwords, width=600, height=500)
    wc.generate(text)
    filename = f"wordcloud_{uuid.uuid4().hex}.png"
    wc.to_file(IMAGE_PATH + f'/{filename}')
    return filename
    