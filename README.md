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

# 🎬 YouTube OAuth2 Setup Guide for Auto 4K Uploader

This guide explains how to create your **YouTube OAuth credentials (`client_secret.json`)** so your Python script can upload videos automatically.

---

## 🪜 Step 1 — Open Google Cloud Console
👉 Go to [https://console.cloud.google.com](https://console.cloud.google.com)  
Log in with the same Google account as your YouTube channel.

---

## 🪜 Step 2 — Create a New Project
1. Click the **Project Selector** (top bar) → **New Project**  
2. Name it: `YouTube_Upscale_Uploader`
3. Click **Create**
4. Switch to the new project after it’s created.

---

## 🪜 Step 3 — Enable YouTube Data API v3
1. In the left menu, go to **APIs & Services → Library**
2. Search for **YouTube Data API v3**
3. Click it → **Enable**

---

## 🪜 Step 4 — Create OAuth 2.0 Credentials
1. Go to **APIs & Services → Credentials**
2. Click **+ Create Credentials → OAuth client ID**

   If it asks to configure a consent screen:
   - Choose **External**
   - Fill in:
     - **App name:** `YouTube 4K Uploader`
     - **User support email:** your Gmail
     - **Developer contact email:** same Gmail  
   - Click **Save and Continue** until done.

3. Now create the OAuth client:
   - Application type: **Desktop app**
   - Name: `YouTubeUploaderDesktop`
   - Click **Create**

---

## 🪜 Step 5 — Download and Rename JSON
1. After creation, click the **Download icon** next to your OAuth client.
2. Rename the file to: client_secret.json
3. Move it to your project root

---

## 🪜 Step 6 — Run for the First Time
Run your script: python go.py

It will:
  1.Open a browser window
  2.Ask you to log in and allow access
  3.Save a token file locally (e.g. token.json)
  4.After that, future uploads won’t require login again.

🪜 Step 7 — Verify on YouTube

Check YouTube Studio → Content → Videos
You should see your video uploaded as Unlisted.

