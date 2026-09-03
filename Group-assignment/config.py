"""Central config shared by preset recording and the web app.

Edit ACTIONS to change the vocabulary. Everything else (recording,
live inference) reads from here so they never drift out of sync.
"""
import os

# Static hand-shape signs to recognize (ASL alphabet minus J and Z, which
# require motion and can't be captured as a single still hand shape).
ACTIONS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L", "M", "N",
    "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
]

# Standard ASL fingerspelling hand-shape descriptions, shown in the UI's
# Sign Guide so a presenter/audience knows exactly what to form for each
# letter (and so recordings made with record_presets.py match a real
# reference instead of an arbitrary shape).
SIGN_DESCRIPTIONS = {
    "A": "Fist with thumb resting against the side of the fist (not tucked in front).",
    "B": "Flat hand, four fingers straight up together, thumb folded across the palm.",
    "C": "Hand curved into a 'C' shape, like holding a cup.",
    "D": "Index finger points straight up; thumb touches middle finger, other fingers curl down.",
    "E": "Fingers curled down close together, thumb tucked under the fingertips.",
    "F": "Thumb and index finger touch tips forming a circle; other three fingers point up.",
    "G": "Index finger and thumb point sideways, parallel to each other, other fingers closed.",
    "H": "Index and middle finger extended together sideways, thumb resting on ring finger.",
    "I": "Pinky finger points up; other fingers and thumb are closed in a fist.",
    "K": "Index and middle finger up in a 'V', thumb touches the middle finger's base.",
    "L": "Thumb and index finger form an 'L' shape, other fingers curled into the palm.",
    "M": "Thumb tucked under the index, middle, and ring fingers.",
    "N": "Thumb tucked under the index and middle fingers.",
    "O": "All fingers and thumb curve together to form an 'O' shape.",
    "P": "Like 'K' but pointing downward.",
    "Q": "Like 'G' but pointing downward.",
    "R": "Index and middle finger crossed, other fingers closed.",
    "S": "Fist with thumb wrapped across the front of the fingers.",
    "T": "Fist with thumb tucked between the index and middle finger.",
    "U": "Index and middle finger point up together, side by side.",
    "V": "Index and middle finger point up, spread apart in a 'V'.",
    "W": "Index, middle, and ring fingers point up, spread apart; thumb holds pinky down.",
    "X": "Index finger bent into a hook shape, other fingers closed.",
    "Y": "Thumb and pinky extended outward, other fingers curled ('hang loose' shape).",
}

# Where the recorded reference hand-shape presets are stored.
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
PRESETS_PATH = os.path.join(MODEL_DIR, "sign_presets.json")

# MediaPipe Tasks bundle for hand/pose landmark extraction (downloaded once
# by model/download_assets.py - not bundled with the mediapipe pip package).
HOLISTIC_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/holistic_landmarker/holistic_landmarker/float16/latest/holistic_landmarker.task"
HOLISTIC_MODEL_PATH = os.path.join(MODEL_DIR, "holistic_landmarker.task")

# Max normalized-Euclidean distance between a live hand shape and its
# nearest preset before it's accepted as a match. Lower = stricter.
MATCH_THRESHOLD = 0.35

# How many consecutive frames must agree on the same letter before it's
# emitted, so a fleeting misread doesn't flicker into the transcript.
STABLE_FRAMES_REQUIRED = 6
