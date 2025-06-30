import pandas as pd
import matplotlib.pyplot as plt
from app import IMAGE_PATH
import uuid

# Pie chart dengan persentase dan jumlah
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return f'{pct:.2f}%\n({val})'
    return my_autopct

def diagram_labelling(data):
    sentiment_count = data['Sentiment'].value_counts()
    labels = ['Positif', 'Netral', 'Negatif']
    sizes = [
        sentiment_count.get('Positif', 0),
        sentiment_count.get('Netral', 0),
        sentiment_count.get('Negatif', 0)
    ]
    colors = ['#00b889', '#666e7a', '#f44336']  # Sesuai warna di gambar
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        colors=colors,
        startangle=90,
        autopct=make_autopct(sizes),
        textprops={'fontsize': 10, 'color': 'white', 'fontweight':'bold'}
    )

    # Legenda di bawah
    ax.legend(
        wedges, labels,
        title="Sentimen",
        loc='lower center',
        bbox_to_anchor=(0.5, -0.15),
        ncol=3
    )

    # Judul
    plt.title('Distribusi Sentimen\nMetode InSet Lexicon Based', fontsize=14, pad=20)
    plt.axis('equal')
    plt.tight_layout()
    # Simpan gambar
    filename = f'diagram_labelling_{uuid.uuid4().hex[:8]}.png'
    plt.savefig(IMAGE_PATH + '/' + filename)
    return filename