from app import KAMUS_PATH
import pandas as pd
def replace_taboo_words(tokens, kamus_tidak_baku):
    if isinstance(tokens, list):
        replaced_words = []
        kalimat_baku = []
        kata_diganti = []
        kata_tidak_baku_hash = []

        for word in tokens:
            if word in kamus_tidak_baku:
                baku_word = kamus_tidak_baku[word]
                if isinstance(baku_word, str) and all(char.isalpha() for char in baku_word):
                    replaced_words.append(baku_word)
                    kalimat_baku.append(baku_word)
                    kata_diganti.append(word)
                    kata_tidak_baku_hash.append(hash(word))
            else:
                replaced_words.append(word)

        replaced_text = ' '.join(replaced_words)
    else:
        replaced_text = ''
        kalimat_baku = []
        kata_diganti = []
        kata_tidak_baku_hash = []

    return replaced_text, kalimat_baku, kata_diganti, kata_tidak_baku_hash
def normalisasi_tweet(data):
    kamus_data = pd.read_csv(KAMUS_PATH + '/kamuskatabaku.csv')
    kamus_tidak_baku = dict(zip(kamus_data['tidak_baku'], kamus_data['kata_baku']))
    # Terapkan fungsi pergantian kata tidak baku
    data['normalisasi'], data['Kata_Baku'], data['Kata_Tidak_Baku'], data['Kata_Tidak_Baku_Hash'] = zip(*data['tokenizing'].apply(lambda x: replace_taboo_words(x, kamus_tidak_baku)))

    data = pd.DataFrame(data[['full_text','cleaning','case_folding','tokenizing','normalisasi']])
    return data