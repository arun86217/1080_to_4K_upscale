# Auto 4K Upscaler & YouTube Uploader 🎥

This project automatically:
1. Watches a folder for new gameplay videos.
2. Upscales them to 4K (Intel QSV or CPU fallback).
3. Uploads the result to your YouTube channel as **unlisted**.

---

### 🧩 Tech Stack
- Python 3.11+
- FFmpeg (with QSV)
- Google API (YouTube Data v3)
- Watchdog for folder monitoring

---

### ⚙️ Setup
```bash
pip install -r requirements.txt
