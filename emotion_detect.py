import requests
from deepface import DeepFace
import cv2
from datetime import datetime
from spotify_map import open_spotify

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

# ================= UI =================
TEXT_COLOR = (0, 200, 200)
PROMPT_COLOR = (255, 255, 0)

# ================= STATE =================
last_emotion = None
last_spotify_emotion = None
user_prompt_active = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        result = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False
        )

        raw = result[0]['emotion']

        # ===== CORE 4 EMOTIONS =====
        core_scores = {
            "happy": raw.get("happy", 0),
            "sad": raw.get("sad", 0),
            "neutral": raw.get("neutral", 0),
            "angry": raw.get("angry", 0)
        }

        # ===== MERGE OTHER EMOTIONS =====
        extra = (
            raw.get("fear", 0) +
            raw.get("surprise", 0) +
            raw.get("disgust", 0)
        )

        core_scores["angry"] += extra * 0.6
        core_scores["sad"] += extra * 0.2
        core_scores["neutral"] += extra * 0.2

        # ===== CALIBRATION =====
        core_scores["neutral"] *= 0.85
        core_scores["happy"] *= 0.95
        core_scores["sad"] *= 1.05
        core_scores["angry"] *= 1.30

        # ===== NORMALIZE =====
        total = sum(core_scores.values())
        emotion_scores = {
            emo: (score / total) * 100
            for emo, score in core_scores.items()
        }

        # ===== FINAL EMOTION =====
        emotion = max(emotion_scores, key=emotion_scores.get)
        confidence = emotion_scores[emotion]

        # ===== SEND TO BACKEND (SAFE) =====
        if emotion != last_emotion:
            try:
                requests.post(
                    "http://127.0.0.1:5000/update_emotion",
                    json={
                        "emotion": str(emotion),
                        "confidence": float(confidence)
                    },
                    timeout=0.3
                )
            except requests.exceptions.RequestException:
                pass

            # ===== TERMINAL LOG =====
            time_now = datetime.now().strftime("%H:%M:%S")
            print(f"[INFO] {time_now}")
            print("Emotion probabilities:")
            for emo, score in emotion_scores.items():
                print(f"  {emo}: {score:.1f}%")
            print(f"[FINAL] Dominant emotion: {emotion}\n")

            user_prompt_active = True
            last_emotion = emotion

        # ================= UI =================
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (380, 140), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.25, frame, 0.75, 0)

        cv2.putText(
            frame,
            f"{emotion.upper()} ({confidence:.1f}%)",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            TEXT_COLOR,
            2
        )

        y = 65
        for emo, score in emotion_scores.items():
            cv2.putText(
                frame,
                f"{emo}: {score:.1f}%",
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (200, 200, 200),
                1
            )
            y += 18

        if user_prompt_active:
            cv2.putText(
                frame,
                "Need music for your mood?  Y = Yes | N = No",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                PROMPT_COLOR,
                1
            )

    except Exception as e:
        print("[ERROR]", e)

    cv2.imshow("Emotion AI (4-Emotion Model)", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('y') and user_prompt_active:
        if emotion != last_spotify_emotion:
            open_spotify(emotion)
            last_spotify_emotion = emotion
        user_prompt_active = False

    elif key == ord('n') and user_prompt_active:
        user_prompt_active = False

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
