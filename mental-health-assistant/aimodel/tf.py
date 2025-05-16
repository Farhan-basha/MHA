from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Load emotion recognition model
model = load_model('emotion_detection_model.h5')

# Define emotion labels
emotion_labels = ['Happy', 'Sad', 'Angry', 'Scared']

# OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    """Capture video frame-by-frame and analyze emotions."""
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face_roi = gray[y:y+h, x:x+w]

                # Resize for model input
                face_roi = cv2.resize(face_roi, (48, 48))
                face_roi = np.expand_dims(face_roi, axis=0)
                face_roi = np.expand_dims(face_roi, axis=-1)
                face_roi = face_roi / 255.0

                # Predict emotion
                predictions = model.predict(face_roi)
                emotion_idx = np.argmax(predictions)
                emotion = emotion_labels[emotion_idx]
                confidence = np.max(predictions) * 100

                # Draw bounding box & label
                text = f"{emotion} ({confidence:.2f}%)"
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Encode frame to send via HTTP
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    return "Flask server is running"

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Trigger analysis manually (if needed)"""
    return jsonify({'result': 'Emotion Analysis Running'})


if __name__ == '__main__':
    app.run(debug=True)
