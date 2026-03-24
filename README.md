# 🎬 CaptionFlow – AI Video Subtitle Generator

CaptionFlow is an AI-powered Streamlit web application that automatically generates subtitles from uploaded videos.
It can transcribe speech, translate subtitles into different languages, and provide downloadable subtitle and transcript files.

The app uses Faster-Whisper for speech recognition and Deep-Translator for multilingual subtitle conversion.

## 🚀 Live App

https://rishiketpagi-captionflow.streamlit.app

## 📂 GitHub Repository

https://github.com/rishiketpagi/captionflow

---

## ✨ Features

* Upload video files (`.mp4`, `.mov`, `.avi`, `.mkv`)
* Extract audio automatically from video
* AI speech-to-text transcription
* Generate timestamped `.srt` subtitle files
* Convert subtitles to other languages
* Copyable transcript text output
* Download transcript as `.txt`
* Download subtitles as `.srt`
* Audio language selection
* Subtitle output language selection
* Modern glass-style UI
* Works directly in browser (no local UI needed)

---

## 🌍 Supported Languages

Audio Language (input):

* Auto Detect
* English
* Hindi
* Marathi
* Tamil
* Telugu
* Bengali
* Spanish
* French
* German

Subtitle Output Language:

* Original
* English
* Hindi
* Marathi
* Tamil
* Telugu
* Bengali
* Spanish
* French
* German

Example:

English audio → Hindi subtitles
Hindi audio → English subtitles
Auto detect → Translate to selected language

---

## 🧠 Tech Stack

* Python
* Streamlit
* Faster-Whisper
* MoviePy
* ImageIO (FFmpeg)
* Deep-Translator
* Custom CSS UI

---

## 📸 Screenshot

![Screenshot](image.png)

---

## ⚙️ Run Locally

Clone repository

```bash
git clone https://github.com/rishiketpagi/captionflow.git
cd captionflow
```

Create virtual environment

```bash
python -m venv venv
```

Activate (Windows)

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run app

```bash
streamlit run app.py
```

---

## ☁️ Deployment

This project is deployed using Streamlit Community Cloud.

Steps used:

1. Push project to GitHub
2. Open Streamlit Community Cloud
3. Connect GitHub repo
4. Select `app.py`
5. Deploy

---

## 📌 Notes

* Use short videos for best performance on cloud
* Tiny model is recommended for faster results
* Translation quality depends on audio clarity
* Large videos may take longer to process
* Free cloud has limited CPU

---

## 👨‍💻 Author

Rishiket Pagi

GitHub
https://github.com/rishiketpagi

LinkedIn
https://www.linkedin.com/in/rishiket-pagi
