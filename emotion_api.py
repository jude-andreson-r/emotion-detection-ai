from flask import Flask, jsonify
from deepface import DeepFace
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(0)

last_emotion = "neutral"
last_confidence = 0.0

def detect_emotion():
    global last_emotion, last_confidence

    ret, frame = cap.read()
    if not ret:
        return

    result = DeepFace.analyze(
        frame,
        actions=['emotion'],
        enforce_detection=False
    )

    emotion = result[0]['dominant_emotion']
    confidence = result[0]['emotion'][emotion]

    last_emotion = emotion
    last_confidence = float(confidence)

@app.route("/emotion", methods=["GET"])
def get_emotion():
    detect_emotion()
    return jsonify({
        "emotion": last_emotion,
        "confidence": last_confidence
    })

if __name__ == "__main__":
    app.run(port=5001)
