
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import time

# Definisikan path yang bisa diakses di semua file
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TWEETS_DATA_PATH = os.path.join(BASE_PATH, '..', 'tweets-data')
UPLOAD_PATH = os.path.join(BASE_PATH, '..', 'uploads')
KAMUS_PATH = os.path.join(BASE_PATH, '..', 'kamus')
IMAGE_PATH = os.path.join(BASE_PATH, '..', 'images')

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

from app import routes
from app import sockets