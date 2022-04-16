import codecs
import base64
import json
import os
import uuid
import numpy as np
import face_recognition as fr
from PIL import Image
import cv2 as cv
from deepface import DeepFace
from datetime import datetime as dt
from flask import Flask, jsonify, render_template, request
backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]

app = Flask(__name__)
global free
free = True

# def checkFree():
#     if False in free:
#         return True
#     else:
#         return False

# def freeOneOfThread():
#     for i in range(len(free) - 1):
#         if free[i] == False:
#             free[i] = True

# def bindOneOfThreads():
#     for i in range(len(free) - 1):
#         if free[i] == True:
#             print([free, i])
#             free[i] = False

@app.route('/')
def index():
    return render_template('index.html')

def archive():
    return render_template('archive.html')

@app.route('/send_image', methods=['POST'])
def result():
    global free
    if request.method == 'POST':
        req = request.get_data().decode("utf-8")
        result = json.loads(req)['image'][22:]
        result = base64.b64decode(result)
        req = cv.imdecode(np.fromstring(result, np.uint8), cv.IMREAD_COLOR)
        small_frame = cv.resize(req, (0, 0), None, 0.25, 0.25)
        if free == False:
            return jsonify({"err": "bussy", "code": 0})
        free = False
        try:
            result = DeepFace.analyze(
                small_frame, actions=["age", "gender", "emotion", "race"], detector_backend=backends[5], )
        except ValueError:
            free = True
            return jsonify({"err": "No face", "code": 0})
        free = True
        return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context=(
        'cert.pem', 'key.pem'),  debug=True)
