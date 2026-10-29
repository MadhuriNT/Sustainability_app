# 🌱 SustainIQ — Germany Student Guide

An AI-powered Streamlit app for sustainability students in Germany.

---

## 📁 Files in this folder

| File | What it does |
|------|-------------|
| `app.py` | The entire Python app (all 7 pages) |
| `requirements.txt` | List of Python packages needed |
| `Dockerfile` | Recipe to build the Docker container |
| `.dockerignore` | Files to exclude from Docker build |

---

## 🚀 How to run (2 ways)

### WAY 1 — Run with Python directly (easier, no Docker needed)

**Step 1 — Install Python 3.11+**
Download from https://python.org

**Step 2 — Install packages**
Open terminal in this folder and run:
```
pip install -r requirements.txt
```

**Step 3 — Run the app**
```
streamlit run app.py
```

**Step 4 — Open browser**
Go to: http://localhost:8501

---

### WAY 2 — Run with Docker (recommended for sharing)

**Step 1 — Install Docker**
Download from https://docker.com/get-started

**Step 2 — Open terminal in this folder**
```
cd sustainiq_app
```

**Step 3 — Build the image**
```
docker build -t sustainiq .
```
This takes ~2 minutes the first time (downloading Python + packages).

**Step 4 — Run the container**
```
docker run -p 8501:8501 sustainiq
```

**Step 5 — Open browser**
Go to: http://localhost:8501

**To stop the app:**
Press Ctrl+C in the terminal.

---

## 🤖 AI Chat — Important Note

The AI Chat on the Home page calls the Anthropic Claude API.
The API key is handled automatically if you run this inside Claude.ai.

If you run it locally on your own machine, the AI chat will show
a connection error — this is normal. All other tabs (Disasters,
Jobs, Part-time, Climate, Energy, Visa) work without any API key.

---

## 📄 Pages in the app

| Page | Content |
|------|---------|
| 🏠 Home & AI Chat | Ask AI about student life in Germany |
| 🌍 European Disasters | 1975–2025 disaster data with charts |
| 💼 Sustainability Jobs | Careers, salaries, skills |
| ⏰ Part-time Work | Rules, jobs, earnings calculator |
| 🌡️ Climate Data | Temperature & CO₂ trends |
| ⚡ Green Energy | Germany Energiewende data |
| 🪪 Visa & Stay | Student visa step-by-step guide |
