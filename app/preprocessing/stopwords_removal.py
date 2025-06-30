from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import pandas as pd
# Inisialisasi stopword remover dari Sastrawi
factory = StopWordRemoverFactory()
sastrawi_stopwords = set(factory.get_stop_words())

# Stopwords tambahan dari media sosial
custom_stopwords = {
    'aja', 'nih', 'sih', 'dong', 'deh', 'gue', 'lu', 'rt', 'jd', 'jg', 'ouh',
    'gak', 'ga', 'nggak', 'btw', 'wkwk', 'ckckck', 'ckck', 'wkjokwaowkoakwa', 'cie', 'haha', 'hehe', 'ampun',
    'mas', 'mbak', 'om', 'tante', 'bro', 'sis', 'ya', 'lho', 'klo', 'padahal', 'noh', 'pas', 'oiya', 'ok', 'ah', 'awkowkwk',
}

# Gabungkan semua stopwords
all_stopwords = sastrawi_stopwords.union(custom_stopwords)

def remove_stopwords(text, stopwords_set):
    if isinstance(text, str):
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords_set]
        return ' '.join(filtered_words)
    else:
        return ''

def stopwords_removal_tweet(data):
    # Kembalikan DataFrame dengan kolom yang relevan
    data = pd.DataFrame(data[['full_text','cleaning','case_folding','tokenizing','normalisasi']])
    data['stopwords_removal'] = data['normalisasi'].apply(lambda x: remove_stopwords(x, all_stopwords))
    return data