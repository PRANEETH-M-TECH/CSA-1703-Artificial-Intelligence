"""Shared MediaPipe Holistic Landmarker (Tasks API) helpers: hand landmark
extraction, normalization, and nearest-preset matching.

Used by both the preset recording script and the live Flask app so the
feature vector format is always identical between recording and inference.

Note: mediapipe's pip package (1.0+) dropped the old `mp.solutions.holistic`
API in favor of the Tasks API used here, which requires a downloaded model
bundle - see model/download_assets.py.
"""
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.core.base_options import BaseOptions

from config import HOLISTIC_MODEL_PATH

# 21 hand landmarks * 3 (x, y, z)
HAND_LEN = 21 * 3

# Landmark indices used to make the hand vector position/scale invariant:
# wrist (0) is the origin, middle-finger-MCP (9) distance sets the scale.
WRIST_IDX = 0
SCALE_REF_IDX = 9


def create_holistic_landmarker():
    """Create a HolisticLandmarker (image mode). Usable as a context manager."""
    options = mp_vision.HolisticLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=HOLISTIC_MODEL_PATH),
        running_mode=mp_vision.RunningMode.IMAGE,
    )
    return mp_vision.HolisticLandmarker.create_from_options(options)


def mediapipe_detection(image_rgb, landmarker):
    """Run one RGB frame (numpy array) through the landmarker, return results."""
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    return landmarker.detect(mp_image)


def normalize_hand(landmarks) -> np.ndarray:
    """Turn a list of 21 hand landmarks into a translation/scale invariant
    vector, so the same hand shape matches regardless of where the hand is
    in frame or how close it is to the camera.
    """
    pts = np.array([[p.x, p.y, p.z] for p in landmarks])
    origin = pts[WRIST_IDX]
    pts = pts - origin
    scale = np.linalg.norm(pts[SCALE_REF_IDX]) or 1.0
    pts = pts / scale
    return pts.flatten()


def extract_hand_shape(results):
    """Return (hand_label, normalized_vector) for whichever hand is visible.

    Prefers the right hand when both are visible (presets are recorded
    one-handed). Returns (None, None) if no hand is detected.
    """
    if results.right_hand_landmarks:
        return "right", normalize_hand(results.right_hand_landmarks)
    if results.left_hand_landmarks:
        return "left", normalize_hand(results.left_hand_landmarks)
    return None, None


def match_preset(vector, presets: dict):
    """Find the nearest preset to `vector` by Euclidean distance.

    presets: {label: [flattened normalized 63-length vector], ...}
    Returns (best_label, best_distance) or (None, None) if presets is empty.
    """
    if not presets or vector is None:
        return None, None

    best_label, best_dist = None, float("inf")
    for label, preset_vector in presets.items():
        dist = float(np.linalg.norm(vector - np.array(preset_vector)))
        if dist < best_dist:
            best_label, best_dist = label, dist
    return best_label, best_dist


# Landmark index pairs to connect when drawing a hand skeleton (thumb,
# fingers, palm) - mirrors the classic MediaPipe hand topology as plain
# tuples so the frontend doesn't need MediaPipe's JS build to draw the
# overlay.
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),          # thumb
    (0, 5), (5, 6), (6, 7), (7, 8),          # index
    (5, 9), (9, 10), (10, 11), (11, 12),     # middle
    (9, 13), (13, 14), (14, 15), (15, 16),   # ring
    (13, 17), (17, 18), (18, 19), (19, 20),  # pinky
    (0, 17),                                  # palm base
]


def landmarks_for_overlay(results):
    """Return just (x, y) points for hands the frontend can draw on a
    canvas overlay, so the UI visibly shows what's being tracked."""

    def to_xy(landmark_list):
        if not landmark_list:
            return []
        return [[p.x, p.y] for p in landmark_list]

    return {
        "left_hand": to_xy(results.left_hand_landmarks),
        "right_hand": to_xy(results.right_hand_landmarks),
        "connections": HAND_CONNECTIONS,
    }
