"""One-time download of the MediaPipe Holistic Landmarker model bundle.

MediaPipe's pip package no longer ships this model file (it moved to the
Tasks API), so it must be fetched once before collect_data.py, train_model.py,
or app.py can run. Requires an internet connection; run once per machine:

    python model/download_assets.py
"""
import os
import sys
import urllib.request

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import HOLISTIC_MODEL_URL, HOLISTIC_MODEL_PATH


def main():
    if os.path.exists(HOLISTIC_MODEL_PATH):
        print(f"Already present: {HOLISTIC_MODEL_PATH}")
        return

    os.makedirs(os.path.dirname(HOLISTIC_MODEL_PATH), exist_ok=True)
    print(f"Downloading {HOLISTIC_MODEL_URL} ...")
    urllib.request.urlretrieve(HOLISTIC_MODEL_URL, HOLISTIC_MODEL_PATH)
    print(f"Saved to {HOLISTIC_MODEL_PATH}")


if __name__ == "__main__":
    main()
