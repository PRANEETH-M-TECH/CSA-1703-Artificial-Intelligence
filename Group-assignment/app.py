"""Flask web app: browser webcam -> MediaPipe hand landmarks -> nearest-
preset sign matching -> recognized letter sent back to the browser, which
speaks it using the Web Speech API (no server-side audio needed).

No training step: signs are matched against reference shapes recorded by
model/record_presets.py (model/sign_presets.json).

Run: python app.py, then open http://127.0.0.1:5000
"""
import os
import json
import base64
from collections import deque

import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify

from config import (
    MATCH_THRESHOLD, STABLE_FRAMES_REQUIRED, PRESETS_PATH,
    ACTIONS, SIGN_DESCRIPTIONS, HOLISTIC_MODEL_PATH,
)
from utils.mediapipe_utils import (
    create_holistic_landmarker, mediapipe_detection, extract_hand_shape,
    match_preset, landmarks_for_overlay,
)

if not os.path.exists(HOLISTIC_MODEL_PATH):
    raise SystemExit(
        f"Missing {HOLISTIC_MODEL_PATH}.\n"
        "Download it first - see README.md."
    )

app = Flask(__name__)

# --- Load recorded presets (if any exist yet) -------------------------------
presets = {}
if os.path.exists(PRESETS_PATH):
    with open(PRESETS_PATH) as f:
        presets = json.load(f)
else:
    print("WARNING: no presets recorded yet. Run model/record_presets.py "
          "before predictions will work.")

# --- Shared MediaPipe instance + small stability buffer ---------------------
# NOTE: single global state -> fine for a local single-user demo. Not safe
# for multiple simultaneous users; that's out of scope for this project.
holistic = create_holistic_landmarker()
recent_labels = deque(maxlen=STABLE_FRAMES_REQUIRED)
last_word = None


def decode_image(data_url: str) -> np.ndarray:
    header, encoded = data_url.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


@app.route("/")
def index():
    sign_guide = [
        {"word": a, "recorded": a in presets, "description": SIGN_DESCRIPTIONS.get(a, "")}
        for a in ACTIONS
    ]
    return render_template("index.html", sign_guide=sign_guide)


@app.route("/predict", methods=["POST"])
def predict():
    global last_word

    payload = request.get_json(silent=True) or {}
    data_url = payload.get("image")
    if not data_url:
        return jsonify({"error": "No image provided"}), 400

    frame = decode_image(data_url)
    if frame is None:
        return jsonify({"error": "Could not decode image"}), 400

    # Mirror to match record_presets.py, which also mirrors before detection
    # (and matches what the signer sees on the CSS-mirrored <video> element).
    # Without this, live landmarks are a left-right flip of the recorded
    # presets and nothing matches even for the same hand shape.
    frame = cv2.flip(frame, 1)
    image_rgb = np.ascontiguousarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    results = mediapipe_detection(image_rgb, holistic)
    landmarks = landmarks_for_overlay(results)

    if not presets:
        return jsonify({"error": "No signs recorded yet. See README.", "landmarks": landmarks}), 503

    _, vector = extract_hand_shape(results)
    if vector is None:
        recent_labels.clear()
        return jsonify({"word": None, "landmarks": landmarks})

    label, distance = match_preset(vector, presets)
    confidence = max(0.0, 1 - distance / MATCH_THRESHOLD)

    if distance > MATCH_THRESHOLD:
        recent_labels.clear()
        return jsonify({"word": None, "confidence": confidence, "landmarks": landmarks})

    recent_labels.append(label)

    # Only emit once the same letter has been held steady for several
    # frames in a row, and only when it changes - avoids flicker/repeats.
    is_stable = len(recent_labels) == STABLE_FRAMES_REQUIRED and len(set(recent_labels)) == 1
    if not is_stable or label == last_word:
        return jsonify({"word": None, "confidence": confidence, "landmarks": landmarks})

    last_word = label
    return jsonify({"word": label, "confidence": confidence, "landmarks": landmarks})


@app.route("/reset", methods=["POST"])
def reset():
    global last_word
    recent_labels.clear()
    last_word = None
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
