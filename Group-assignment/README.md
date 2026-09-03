# Automated Sign Language Recognition and Speech Conversion System

Recognizes static ASL hand shapes (the alphabet, A-Y excluding J/Z which
need motion) from a webcam in the browser and speaks the recognized letter
aloud using the browser's built-in text-to-speech.

## Pipeline

```
Browser webcam
  -> JPEG frame sent to Flask every ~150ms
  -> MediaPipe Holistic Landmarker extracts hand landmarks (server-side)
  -> hand shape normalized (translation + scale invariant)
  -> compared against recorded reference shapes (nearest match, no training)
  -> if held steady for a few frames, recognized letter sent to browser
  -> browser speaks it (Web Speech API) and adds it to the transcript
```

No neural network training is involved: each sign is just one recorded
reference hand shape (a JSON preset), matched at runtime by nearest
distance. This keeps setup fast and easy to explain in a report.

## One-time setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Download the hand-tracking model (one time, needs internet)

MediaPipe's pip package doesn't bundle its landmark-detection model file
anymore, so it has to be downloaded once:

```bash
python model/download_assets.py
```

If that fails with a DNS/network error (common on campus wifi that
proxies browsers but not other apps), download it manually instead:

1. Open this URL in your normal browser:
   `https://storage.googleapis.com/mediapipe-models/holistic_landmarker/holistic_landmarker/float16/latest/holistic_landmarker.task`
2. Save the downloaded file as `model/holistic_landmarker.task` in this project.

## 1. Record reference signs

Edit the vocabulary list in [config.py](config.py) (`ACTIONS`) if you want
a different set of signs.

```bash
python model/record_presets.py
```

For each letter it shows a live webcam window. Hold the ASL hand shape for
that letter steady, then press **SPACE** to capture it (**ESC** to skip a
letter, **Q** to quit early and save what you've captured so far). Re-run
the script any time to add/overwrite signs — it keeps previously recorded
ones.

## 2. Run the web app

```bash
python app.py
```

Open `http://127.0.0.1:5000`, click **Start Camera**, and hold a recorded
hand shape steady. The Sign Guide panel shows which letters are recorded
(green) vs. still missing (grey). Once matched confidently, the app shows
the letter, speaks it, and appends it to the transcript.

## Project structure

```
app.py                     Flask server: /predict endpoint, live inference
config.py                   Shared vocabulary + thresholds
utils/mediapipe_utils.py    Landmark extraction, normalization, matching
model/download_assets.py    One-time download of the MediaPipe model file
model/record_presets.py     Records one reference hand shape per sign
model/sign_presets.json     Recorded reference shapes (generated, gitignored)
templates/index.html        Web UI
static/js/main.js           Webcam capture loop, calls /predict, speaks result
static/css/style.css        Styling
```

## Known limitations (worth mentioning in the report)

- Static hand shapes only — letters that require motion (J, Z) aren't
  supported by this single-frame matching approach.
- Nearest-preset matching is simple and fast to set up, but less robust
  than a trained classifier to variation in hand angle/lighting; each
  sign should ideally be re-recorded if accuracy is poor for a given signer.
- Single global prediction state in `app.py` — fine for a local one-user
  demo, not safe for concurrent multi-user sessions.
- Runs fully offline/locally after the one-time model download; no
  deployment step required for the demo.
