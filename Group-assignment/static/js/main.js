const video = document.getElementById("webcam");
const canvas = document.getElementById("capture-canvas");
const ctx = canvas.getContext("2d");
const overlay = document.getElementById("overlay-canvas");
const overlayCtx = overlay.getContext("2d");
const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const clearBtn = document.getElementById("clear-btn");
const speakToggle = document.getElementById("speak-toggle");
const statusEl = document.getElementById("status");
const currentWordEl = document.getElementById("current-word");
const transcriptEl = document.getElementById("transcript");
const confidenceFill = document.getElementById("confidence-fill");

let stream = null;
let pollTimer = null;
const POLL_INTERVAL_MS = 150; // ~6-7 fps sent to the server

function speak(text) {
  if (!speakToggle.checked) return;
  const utterance = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(utterance);
}

function drawLandmarks(landmarks) {
  overlay.width = video.videoWidth;
  overlay.height = video.videoHeight;
  overlayCtx.clearRect(0, 0, overlay.width, overlay.height);
  if (!landmarks) return;

  const drawHand = (points, color) => {
    if (!points || points.length === 0) return;
    const px = points.map(([x, y]) => [x * overlay.width, y * overlay.height]);

    overlayCtx.strokeStyle = color;
    overlayCtx.lineWidth = 2;
    for (const [a, b] of landmarks.connections) {
      if (!px[a] || !px[b]) continue;
      overlayCtx.beginPath();
      overlayCtx.moveTo(px[a][0], px[a][1]);
      overlayCtx.lineTo(px[b][0], px[b][1]);
      overlayCtx.stroke();
    }

    overlayCtx.fillStyle = color;
    for (const [x, y] of px) {
      overlayCtx.beginPath();
      overlayCtx.arc(x, y, 4, 0, 2 * Math.PI);
      overlayCtx.fill();
    }
  };

  drawHand(landmarks.left_hand, "#4ade80");
  drawHand(landmarks.right_hand, "#60a5fa");
}

function setConfidence(confidence) {
  const pct = confidence ? Math.round(confidence * 100) : 0;
  confidenceFill.style.width = pct + "%";
}

function appendToTranscript(word) {
  const span = document.createElement("span");
  span.className = "word";
  span.textContent = word;
  transcriptEl.appendChild(span);
  transcriptEl.scrollTop = transcriptEl.scrollHeight;
}

async function captureAndSend() {
  if (!stream) return;
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.7);

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: dataUrl }),
    });
    const data = await res.json();

    if (data.error) {
      statusEl.textContent = data.error;
      drawLandmarks(data.landmarks);
      return;
    }
    drawLandmarks(data.landmarks);
    setConfidence(data.confidence);

    if (data.word) {
      statusEl.textContent = `Recognized: ${data.word} (confidence ${(data.confidence * 100).toFixed(0)}%)`;
      currentWordEl.textContent = data.word;
      appendToTranscript(data.word);
      speak(data.word);
    } else if (data.confidence) {
      statusEl.textContent = `Hold steady... (best match confidence ${(data.confidence * 100).toFixed(0)}%)`;
    } else {
      statusEl.textContent = "Watching for a hand...";
    }
  } catch (err) {
    statusEl.textContent = "Prediction request failed: " + err.message;
  }
}

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    startBtn.disabled = true;
    stopBtn.disabled = false;
    statusEl.textContent = "Camera started. Watching...";
    pollTimer = setInterval(captureAndSend, POLL_INTERVAL_MS);
  } catch (err) {
    statusEl.textContent = "Could not access webcam: " + err.message;
  }
}

async function stopCamera() {
  if (pollTimer) clearInterval(pollTimer);
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    stream = null;
  }
  await fetch("/reset", { method: "POST" });
  startBtn.disabled = false;
  stopBtn.disabled = true;
  statusEl.textContent = "Camera stopped.";
  currentWordEl.textContent = "—";
}

startBtn.addEventListener("click", startCamera);
stopBtn.addEventListener("click", stopCamera);
clearBtn.addEventListener("click", () => {
  transcriptEl.innerHTML = "";
});
