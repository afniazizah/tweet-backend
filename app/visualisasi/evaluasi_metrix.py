import uuid
from matplotlib import pyplot as plt
import pandas as pd
from app import IMAGE_PATH


def evaluasi_metrix(acc, prec, rec, f1):
    metrics = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Score': [acc, prec, rec, f1]
    })
    plt.figure(figsize=(6, 5))
    bars = plt.bar(metrics['Metric'], metrics['Score'], color=['#4285F4', '#34A853', '#FBBC05', '#9966CC'])
    # Menambahkan label nilai di atas setiap bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2%}', va='bottom', ha='center')
    # Kustomisasi plot
    plt.ylim(0, 1.1) # Set limit sumbu y hingga 110%
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    filename = f'evaluation_metrics_{uuid.uuid4().hex[:8]}.png'
    plt.savefig(IMAGE_PATH + '/' + filename)
    plt.close()  # Tutup plot untuk menghindari tampilan berulang
    return filename