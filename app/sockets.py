from app import app, TWEETS_DATA_PATH, BASE_PATH
import subprocess
import random
import string
import os
from app import socketio, emit, eventlet
from app.preprocessing.cleaning import clean_tweet
from app.preprocessing.casefolding import case_folding_tweet
from app.preprocessing.tokenizing import tokenizing_tweet
from app.preprocessing.normalisasi import normalisasi_tweet
from app.preprocessing.stopwords_removal import stopwords_removal_tweet
from app.preprocessing.stemming import stemming_tweet
from app.preprocessing.translate import translate_all
from app.visualisasi.word_cloud import word_cloud_tweet
from app.perhitungan.labelling_tweet import labelling_tweet
from app.visualisasi.diagram_labelling import diagram_labelling
from app.perhitungan.klasifikasi_svm import klasifikasi_svm
import pandas as pd
import time

# result_cleaning = clean_tweet(os.path.join(TWEETS_DATA_PATH, 'data-percobaan.csv'))
# result_case_folding = case_folding_tweet(result_cleaning)
# result_tokenizing = tokenizing_tweet(result_case_folding)
# result_normalisasi = normalisasi_tweet(result_tokenizing)
# result_stopwords_removal = stopwords_removal_tweet(result_normalisasi)
# result_stemming = stemming_tweet(result_stopwords_removal)
# result_stemming.to_csv(TWEETS_DATA_PATH + '/hasil-preprocessing.csv', index=False)
# result_stemming = pd.read_csv(TWEETS_DATA_PATH + '/hasil-preprocessing.csv')
# result_labeling = labelling_tweet(result_stemming)
# klasifikasi_svm(result_labeling)

# diagram_labelling_file = diagram_labelling(result_labeling)
# wordCloudFile =  word_cloud_tweet(result_stemming)

@socketio.on("analisis")
def analisisPerhitungan(params):
    filename = params[0]
    language = params[1]
    st = time.time()
    if language == "en":
        emit("update analisis", "Menerjemahkan Tweet.....")
        eventlet.sleep(0)
        filename = translate_all(TWEETS_DATA_PATH + '/' + filename)
    emit("update analisis", "Cleaning.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_cleaning = clean_tweet(TWEETS_DATA_PATH + '/' + filename)
    emit("update analisis", "Case Folding.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_case_folding = case_folding_tweet(result_cleaning)
    emit("update analisis", "Tokenizing.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_tokenizing = tokenizing_tweet(result_case_folding)
    emit("update analisis", "Normalisasi.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_normalisasi = normalisasi_tweet(result_tokenizing)
    emit("update analisis", "Stopwords Removal.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_stopwords_removal = stopwords_removal_tweet(result_normalisasi)
    emit("update analisis", "Stemming.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_stemming = stemming_tweet(result_stopwords_removal)
    emit("update analisis", "Labelling.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_labeling = labelling_tweet(result_stemming)
    print(result_labeling['Sentiment'].value_counts())
    emit("update analisis", "TF-IDF.....")
    eventlet.sleep(0) # Non-blocking sleep
    emit("update analisis", "Klasifikasi.....")
    eventlet.sleep(0) # Non-blocking sleep
    result_klasifikasi = klasifikasi_svm(result_labeling)
    emit("update analisis", "Visualisasi.....")
    word_cloud_file = word_cloud_tweet(result_stemming)
    result_klasifikasi["word_cloud"] = word_cloud_file
    elapsed_time = time.time() - st
    if elapsed_time >= 60:
        process_time = time.strftime("%M Menit %S detik", time.gmtime(elapsed_time))
    else:
        process_time = time.strftime("%S detik", time.gmtime(elapsed_time))
    result_klasifikasi["process_time"] = process_time
    result_klasifikasi["jumlah_data"] = len(result_cleaning)
    emit('finish analisis', result_klasifikasi)


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
    
@socketio.on("crawl")
def crawl(request):
    auth_token = request["auth_token"]
    keyword = request["keyword"]
    limit = request["limit"]
    sinceDate = request["since_date"]
    untilDate = request["until_date"]
    percentCompelte = 0

    filename = keyword + generate_random_string(10) + '.csv'
    command = f'npx -y tweet-harvest@2.6.1 -o "{filename}" -s "{keyword}{f" since:{sinceDate}" if sinceDate else ""}{f" until:{untilDate}" if untilDate else ""} lang:id" --tab "LATEST" -l "{limit}" --token "{auth_token}"'
    prcoess_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    filename = filename.replace(" ", "_")
    no_more_tweets = False
    total_tweet = 0
    while True:
        baris = prcoess_command.stdout.readline()
        print("Output:", baris.strip())
        if not baris:
            break
        if "Total tweets saved" in baris:
            baris_split = baris.split(": ")
            total_tweet = int(baris_split[1].strip())
            percentCompelte = round((total_tweet / int(limit)) * 100, 2)
            if percentCompelte > 100:
                percentCompelte = 100
            emit("update percent", percentCompelte, broadcast=True)
        elif "done scrolling" in baris:
            percentCompelte = 100
            emit("update percent", percentCompelte, broadcast=True)
        elif "No more tweets found" in baris:
            emit("error crawl", "Tidak ada lagi tweet yang ditemukan. Tweet yang berhasil diambil: " + str(total_tweet), broadcast=True)
            prcoess_command.kill()
            if percentCompelte > 0:
                emit("complete crawl", {
                    "filename": filename,
                    "total_tweet": total_tweet
                }, broadcast=True)
            return
        elif "rate limit" in baris:
            emit("error crawl", "Rate limit terlampaui, Tweet yang berhasil diambil: " + str(total_tweet), broadcast=True)
            if percentCompelte > 0:
                emit("complete crawl", {
                    "filename": filename,
                    "total_tweet": total_tweet
                }, broadcast=True)
            prcoess_command.kill()
            return

    stderr = prcoess_command.stderr.read()
    if stderr or no_more_tweets:
        print("Masuk Ke Error")
        prcoess_command.kill()
        if "token" in stderr:
            emit("error crawl", "Terjadi Kesalahan : Auth token tidak valid", broadcast=True)
        elif "error" in stderr:
            emit("error crawl", "Terjadi Kesalahan : " + stderr, broadcast=True)
        elif "No more tweets found" in stderr:
            emit("error crawl", "Tidak ada lagi tweet yang ditemukan. Tweet yang berhasil diambil: " + str(total_tweet), broadcast=True)
            if percentCompelte > 0:
                emit("complete crawl", {
                    "filename": filename,
                    "total_tweet": total_tweet
                }, broadcast=True)
        elif "rate limit" in stderr:
            emit("error crawl", "Rate limit terlampaui, Tweet yang berhasil diambil: " + str(total_tweet), broadcast=True)
            if percentCompelte > 0:
                emit("complete crawl", {
                    "filename": filename,
                    "total_tweet": total_tweet
                }, broadcast=True)
        else:
            emit("error crawl", "Terjadi Kesalahan : " + stderr, broadcast=True)
        return
    
    emit("complete crawl", {
        "filename": filename,
                    "total_tweet": total_tweet
    }, broadcast=True)