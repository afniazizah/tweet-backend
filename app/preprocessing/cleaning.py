import pandas as pd
import re

#Fungsi untuk menghapus emoji
def remove_emoji(tweet):
    if tweet is not None and isinstance(tweet, str):
      emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # simbol & piktogram
        u"\U0001F680-\U0001F6FF"  # simbol transportasi & simbol sosial
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # geometric shapes extended
        u"\U0001F800-\U0001F8FF"  # supplemental arrows-c
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U0001F004-\U0001F0CF"  # Miscellaneous Symbols and Pictographs (Additional emoticons)
        u"\U0001F1E0-\U0001F1FF"  # simbol bendera
                          "]+", flags=re.UNICODE)
      return emoji_pattern.sub(r'', tweet)
    else:
      return tweet

# Fungsi untuk menghapus simbol
def remove_symbols(tweet):
    if tweet is not None and isinstance(tweet, str):
      tweet = re.sub(r'[^a-zA-Z0-9\s]', '', tweet) # menghapus semua simbol
    return tweet

# Fungsi untuk menghapus angka
def remove_numbers(tweet):
    if tweet is not None and isinstance(tweet, str):
      tweet = re.sub(r'\d', '', tweet) # menghapus semua angka
    return tweet

# Fungsi untuk menghapus username
def remove_username(text):
    import re
    # Corrected indentation for the return statement
    return re.sub(r'@[^\s]+', '', text) # menghapus semua username

# Fungsi untuk menghapus Hashtag
def remove_hashtag(tweet):
    if tweet is not None and isinstance(tweet, str):
      hashtag_pattern = re.compile(r'#\S+') # menghapus semua Hashtag
      return hashtag_pattern.sub(r'', tweet)
    else:
      return tweet

# Fungsi untuk menghapus URL
def remove_url(tweet):
    if tweet is not None and isinstance(tweet, str):
      url = re.compile(r'http\S+|www\.\S+') # menghapus semua URL
      return url.sub(r'', tweet)
    else:
      return tweet

# Fungsi untuk menghapus HTML
def remove_html(tweet):
    if tweet is not None and isinstance(tweet, str):
      html = re.compile(r'<.*?>') # menghapus semua HTML
      return html.sub(r'', tweet)
    else:
      return tweet

def clean_tweet(file):
    data = pd.read_csv(file)
    data = pd.DataFrame(data[['full_text']])
    data['cleaning'] = data['full_text'].apply(lambda x: remove_url(x))
    data['cleaning'] = data['cleaning'].apply(lambda x: remove_username(x))
    data['cleaning'] = data['cleaning'].apply(lambda x: remove_hashtag(x))
    data['cleaning'] = data['cleaning'].apply(lambda x: remove_html(x))
    data['cleaning'] = data['cleaning'].apply(lambda x: remove_emoji(x))
    data['cleaning'] = data['cleaning'].apply(lambda x: remove_symbols(x))
    data['cleaning'] = data['cleaning'].apply(lambda x: remove_numbers(x))
    return data