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
        return jsonify({"error": "Error: Tidak ada file yang diupload"}), 42
    file = request.files['file']
    table_name = request.form.get('table_name')
    try:
        df = pd.read_csv(file)
        if table_name not in df.columns:
            return jsonify({"error": f"Kolom '{table_name}' tidak ditemukan dalam file"}), 422
        print(df[table_name].head())
        if len(df[table_name]) < 100:
            return jsonify({"error": f"Data harus memiliki minimal 100 baris data"}), 422
        df.rename(columns={table_name: 'full_text'})
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        df.to_csv(TWEETS_DATA_PATH + '/' + filename, index=False)
        return jsonify({"filename": filename}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error: File yang diupload tidak valid"}), 422