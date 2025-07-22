import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import uuid
from app import IMAGE_PATH

def confusion_metrix_image(y_test, y_pred):
        # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=[1, 0, -1])
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlGnBu',
                xticklabels=['Positif', 'Netral', 'Negatif'],
                yticklabels=['Positif', 'Netral', 'Negatif'])
    plt.tight_layout()
    filename = f'confusion_matrix_{uuid.uuid4().hex[:8]}.png'
    plt.savefig(IMAGE_PATH + f'/{filename}')
    plt.close()
    return filename