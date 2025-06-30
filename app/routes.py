from app import app, TWEETS_DATA_PATH, IMAGE_PATH
from flask import jsonify, send_file, request, send_from_directory
import os
import uuid
import pandas as pd

@app.route("/get-file/<filename>")
def getFile(filename):
    return send_file(TWEETS_DATA_PATH + '/' + filename, as_attachment=True)

@app.route("/images/<filename>")
def get_image(filename):
    return send_from_directory(IMAGE_PATH, filename)

@app.route("/upload", methods=["POST"])
def upload_file():
    print(request)
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    table_name = request.form.get('table_name')
    df = pd.read_csv(file)
    if table_name not in df.columns:
        return jsonify({"error": f"Kolom '{table_name}' tidak ditemukan dalam file"}), 422
    df.rename(columns={table_name: 'full_text'})
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    df.to_csv(TWEETS_DATA_PATH + '/' + filename, index=False)
    return jsonify({"filename": filename}), 200