from matplotlib import pyplot as plt
from app import IMAGE_PATH
import uuid

def pie_klasifikasi(jumlah, labels):
    print("====== Membuat Pie Chart Klasifikasi ====")
    print(labels)
    colors = ['#00b889', '#f44336', '#666e7a']  # Hijau, Abu, Merah
    plt.figure(figsize=(6, 5))

    # Format label: 68.82% \n(702)
    def format_label(pct, allvals):
        absolute = int(round(pct/100.*sum(allvals)))
        return f"{pct:.2f}%\n({absolute})"
    
    def change_label(labels):
        return ["Positif" if label == 1 else "Negatif" if label == -1 else "Netral" for label in labels]

    wedges, texts, autotexts = plt.pie(
        jumlah,
        labels=change_label(labels),
        autopct=lambda pct: format_label(pct, jumlah),
        colors=colors,
        startangle=140,
        textprops=dict(color="white", fontsize=9, weight='bold')
    )

    # Judul chart

    # Legenda
    plt.legend(wedges, change_label(labels), loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=3)

    plt.axis('equal')
    filename = f'pie_klasifikasi_{uuid.uuid4().hex[:8]}.png'
    plt.savefig(IMAGE_PATH + '/' + filename)
    plt.close()
    return filename