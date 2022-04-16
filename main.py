import base64
from cgitb import small
import json
from urllib import response
from matplotlib.pyplot import get
import numpy as np
import face_recognition as fr
import mediapipe as mp
from PIL import Image
import cv2 as cv
from deepface import DeepFace
from datetime import datetime as dt
from flask import Flask, jsonify, render_template, request, send_from_directory
backends = ['mediapipe', 'opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
models = ["VGG-Face", "Facenet", "Facenet512",
    "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]

app = Flask(__name__)
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

global free
free = True


@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('static', path)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', backends=backends)


def archive():
    return render_template('archive.html')


def mp_analyze(image):
    with mp_face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5) as face_detection:
                results = face_detection.process(
                    cv.cvtColor(image, cv.COLOR_BGR2RGB))
                if not results.detections:
                    return
                for detection in results.detections:
                    copyImage = image.copy()
                    mp_drawing.draw_detection(copyImage, detection)
                    retval, buffer = cv.imencode('.png', copyImage)
                    png_as_text = base64.b64encode(buffer)
                    return png_as_text


def fr_analyze(image):
    return fr.face_locations(image)

@ app.route('/send_image', methods = ['POST'])
def result():
    global free
    res = {}
    if request.method == 'POST':
        req=request.get_data().decode("utf-8")
        jsonData=json.loads(req)
        actions=jsonData['actions']
        landmarks=jsonData['landmarks']
        backend=jsonData['backend']
        result=jsonData['image'][22:]
        result=base64.b64decode(result)
        req=cv.imdecode(np.fromstring(result, np.uint8), cv.IMREAD_COLOR)
        small_frame=cv.resize(req, (0, 0), None, 0.5, 0.5)
        if free == False:
            return jsonify({"err": "bussy", "code": 0})
        free=False
        try:
            if(len(actions) > 0):
                res=DeepFace.analyze(
                small_frame, actions = actions, detector_backend = backend)
            if (landmarks == True):
                results=mp_analyze(small_frame)
                if(len(res) > 0):
                    res["image"] = "data:image/png;base64," + results.decode("utf-8")
                else:
                    res = {"image" : "data:image/png;base64," + results.decode("utf-8")}
        except ValueError:
            free=True
            return jsonify({"err": "No face", "code": 0})
        except Exception:
            free=True
            return jsonify({"err": "Check backend console", "code": 0})
        free=True
        return res

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 443, ssl_context = (
        'cert.pem', 'key.pem'),  debug = True)
