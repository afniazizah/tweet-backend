from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def stemming_text(text):
    if isinstance(text, str):
        return stemmer.stem(text)
    return ''

def stemming_tweet(data):
    data['stemming'] = data['stopwords_removal'].apply(stemming_text)
    return data