"""Record one reference hand shape per sign in config.ACTIONS.

Run locally: python model/record_presets.py
For each letter, hold the hand shape steady in front of the webcam and
press SPACE to capture it (press R to retry a capture, ESC to skip a
letter, Q to quit early). Saves model/sign_presets.json for the Flask app
to load - no training step needed.
"""
import os
import sys
import json
import cv2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import ACTIONS, PRESETS_PATH, HOLISTIC_MODEL_PATH
from utils.mediapipe_utils import create_holistic_landmarker, mediapipe_detection, extract_hand_shape

if not os.path.exists(HOLISTIC_MODEL_PATH):
    raise SystemExit(
        f"Missing {HOLISTIC_MODEL_PATH}.\n"
        "Download it first - see README.md."
    )


def load_existing_presets():
    if os.path.exists(PRESETS_PATH):
        with open(PRESETS_PATH) as f:
            return json.load(f)
    return {}


def main():
    presets = load_existing_presets()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    with create_holistic_landmarker() as landmarker:
        for letter in ACTIONS:
            captured = False
            while not captured:
                ret, frame = cap.read()
                if not ret:
                    print("Webcam frame read failed.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                image = cv2.flip(frame, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = mediapipe_detection(image_rgb, landmarker)
                hand_label, vector = extract_hand_shape(results)

                status = f"hand detected ({hand_label})" if vector is not None else "no hand detected"
                already = " [already recorded]" if letter in presets else ""
                cv2.putText(image, f"Sign: {letter}{already}", (15, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, status, (15, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2, cv2.LINE_AA)
                cv2.putText(image, "SPACE=capture  ESC=skip  Q=quit", (15, image.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)
                cv2.imshow("Record Presets", image)

                key = cv2.waitKey(10) & 0xFF
                if key == ord(" ") and vector is not None:
                    presets[letter] = vector.tolist()
                    print(f"Captured '{letter}'.")
                    captured = True
                elif key == 27:  # ESC
                    print(f"Skipped '{letter}'.")
                    captured = True
                elif key == ord("q"):
                    cap.release()
                    cv2.destroyAllWindows()
                    save(presets)
                    return

    cap.release()
    cv2.destroyAllWindows()
    save(presets)


def save(presets):
    os.makedirs(os.path.dirname(PRESETS_PATH), exist_ok=True)
    with open(PRESETS_PATH, "w") as f:
        json.dump(presets, f, indent=2)
    print(f"Saved {len(presets)} presets to {PRESETS_PATH}")


if __name__ == "__main__":
    main()
