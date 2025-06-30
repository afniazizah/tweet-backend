import os
from app import socketio, app

# Definisikan path global
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TWEETS_DATA_PATH = os.path.join(BASE_PATH, 'tweets-data')

# Set sebagai environment variable agar bisa diakses di semua file
os.environ['BASE_PATH'] = BASE_PATH
os.environ['TWEETS_DATA_PATH'] = TWEETS_DATA_PATH

if __name__ == '__main__':
    socketio.run(app, debug=True)