from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = "/Users/coder_kashish/Downloads/microPlastics_detection"

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(BASE_DIR, path)

app.run(host='0.0.0.0', port=8080)