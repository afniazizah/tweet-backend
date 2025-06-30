import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns

from app.visualisasi.confusion_metrix_image import confusion_metrix_image
from app.visualisasi.evaluasi_metrix import evaluasi_metrix
from app.visualisasi.pie_klasifikasi import pie_klasifikasi

def klasifikasi_svm(data):
    label_mapping = {'Positif': 1, 'Netral': 0, 'Negatif': -1}
    data['Label'] = data['Sentiment'].map(label_mapping)

    tfidf = TfidfVectorizer(max_features=1000) # Jika data Anda besar, bisa coba max_features yang lebih besar
    X = tfidf.fit_transform(data['stemming']).toarray()
    y = data['Label']

    # Split data 80% train, 20% test
    # Tambahkan stratify=y untuk memastikan distribusi kelas yang serupa di train dan test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

    # SVM dengan kernel linear
    svm = SVC(kernel='linear', C=1.0)
    svm.fit(X_train, y_train)
    y_pred = svm.predict(X_test)

    # Evaluasi
    # Menekan peringatan UndefinedMetricWarning
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)


    # Confusion Matrix
    confusion_file = confusion_metrix_image(y_test, y_pred)

    y_pred_train = svm.predict(X_train)
    accuracy_train = accuracy_score(y_train, y_pred_train)

    # --- BAGIAN UNTUK MEMBUAT BAR CHART HASIL EVALUASI DENGAN PERSENTASE ---
    # Membuat DataFrame dari metrik
    evaluasi_file = evaluasi_metrix(acc, prec, rec, f1)


    # ===================== 6. Hitung Jumlah Prediksi per Label =====================
    hasil_prediksi = pd.Series(y_pred).value_counts()
    labels = hasil_prediksi.index.tolist()
    jumlah = hasil_prediksi.values.tolist()
    total = sum(jumlah)
    # Hitung jumlah positif, netral, negatif
    positif = (sum(y_pred == 1) / total) * 100
    netral = (sum(y_pred == 0) / total) * 100
    negatif = (sum(y_pred == -1) / total) * 100
    print(f"Jumlah Positif: {positif}, Netral: {netral}, Negatif: {negatif}, Total: {total}")
    
    # ===================== 7. Pie Chart =====================
    pie_file = pie_klasifikasi(jumlah, labels)

    return {
        "accuracy": round(acc * 100, 2),  # Mengalikan dengan 100 untuk persentase dengan 2 angka di belakang koma
        "positif": f"{round(positif, 2)}%",
        "netral": f"{round(netral, 2)}%",
        "negatif": f"{round(negatif, 2)}%",
        "total": total,
        "confusion_matrix": confusion_file,
        "evaluasi": evaluasi_file,
        "pie_chart": pie_file,
    }