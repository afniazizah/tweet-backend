import pandas as pd

# Unduh kamus lexicon
positive_url = "https://raw.githubusercontent.com/fajri91/InSet/master/positive.tsv"
negative_url = "https://raw.githubusercontent.com/fajri91/InSet/master/negative.tsv"

def tsv_word_weight_to_dict_pandas(nama_file_tsv):
    """
    Mengubah data TSV dengan header 'word' dan 'weight'
    menjadi satu dictionary {word: weight} menggunakan pandas.
    """
    result_dict = {}
    try:
        # === PERUBAHAN DI SINI: sep='\t' ===
        df = pd.read_csv(nama_file_tsv, sep='\t')

        # Pastikan kolom 'word' dan 'weight' ada
        if 'word' not in df.columns or 'weight' not in df.columns:
            print("Error: File TSV harus memiliki kolom 'word' dan 'weight'.")
            return {}

        df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
        df.dropna(subset=['weight'], inplace=True)

        result_dict = df.set_index('word')['weight'].to_dict()

    except FileNotFoundError:
        print(f"Error: File '{nama_file_tsv}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    return result_dict

positive_lexicon = tsv_word_weight_to_dict_pandas(positive_url)
negative_lexicon = tsv_word_weight_to_dict_pandas(negative_url)

# Fungsi utama menentukan sentimen
def determine_sentiment(text):
    if isinstance(text, str):
        words = text.split()
        positive_count = 0
        negative_count = 0
        for word in words:
            if word in positive_lexicon:
                positive_count += positive_lexicon[word]
            if word in negative_lexicon:
                negative_count += negative_lexicon[word]
        sentiment_score = positive_count + negative_count
        if sentiment_score > 0:
            sentiment = "Positif"
        elif sentiment_score < 0:
            sentiment = "Negatif"
        else:
            sentiment = "Netral"
        return sentiment, sentiment_score
    else:
        return "Netral", 0

# ✅ Fungsi tambahan: daftar kata dengan nilai sentimen
def word_sentiment_list(text):
    result = []
    for word in text.split():
        resultWord = word;
        if word in positive_lexicon:
            resultWord += f"({positive_lexicon[word]})"
        if word in negative_lexicon:
            resultWord += f"({negative_lexicon[word]})"
        if word not in positive_lexicon and word not in negative_lexicon:
            resultWord += "(0)"
        result.append(resultWord)
    return " ".join(result)

def labelling_tweet(data):
    data = pd.DataFrame(data[['stemming']])
    data = data.dropna()
    # Word Count
    data['Word_Count'] = data['stemming'].apply(lambda x: len(str(x).split()))

    # Sentiment & Score
    data[['Sentiment', 'Score']] = data['stemming'].apply(lambda x: pd.Series(determine_sentiment(x)))

    # Word Sentiment Detail
    data['Word_Sentiment_Detail'] = data['stemming'].apply(word_sentiment_list)

    # Tampilkan hasil
    return data[['stemming', 'Sentiment', 'Score', 'Word_Count', 'Word_Sentiment_Detail']]