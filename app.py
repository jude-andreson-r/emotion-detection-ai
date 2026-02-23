from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# GLOBAL STATE
current_emotion = "Waiting for emotion..."
current_confidence = 0.0

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/update_emotion", methods=["POST"])
def update_emotion():
    global current_emotion, current_confidence
    data = request.json

    if data:
        current_emotion = data.get("emotion", current_emotion)
        current_confidence = data.get("confidence", current_confidence)

    return jsonify({"status": "updated"})

@app.route("/emotion", methods=["GET"])
def get_emotion():
    return jsonify({
        "emotion": current_emotion,
        "confidence": current_confidence
    })

if __name__ == "__main__":
    app.run()
