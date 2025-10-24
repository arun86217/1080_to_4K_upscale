import os, glob
from upscale import upscale
from youtube_uploader import upload

INPUT_DIR = r"D:\Personal\1080p_to_4k\videos\input"
OUTPUT_DIR = r"D:\Personal\1080p_to_4k\videos\output"
WORK_DIR   = r"D:\Personal\1080p_to_4k\videos\work"

def latest_video():
    mp4s = glob.glob(os.path.join(INPUT_DIR, "*.mp4"))
    if not mp4s:
        print("No videos found in input folder.")
        return None
    return max(mp4s, key=os.path.getctime)

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(WORK_DIR, exist_ok=True)

    video = latest_video()
    if not video: exit()

    base = os.path.splitext(os.path.basename(video))[0]
    out = os.path.join(OUTPUT_DIR, f"{base}_4k.mp4")

    print(f"Starting upscale → {video}")
    upscale(video, out, workdir=WORK_DIR)
    print(f"Upscale complete → {out}")

    print("Uploading to YouTube as Unlisted...")
    upload(out)
    print("All done!")
