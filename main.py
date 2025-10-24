import time, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from upscale import upscale
from youtube_uploader import upload

INPUT_DIR = r"D:\Personal\1080p_to_4k\videos\input"
OUTPUT_DIR = r"D:\Personal\1080p_to_4k\videos\output"
WORK_DIR   = r"D:\Personal\1080p_to_4k\videos\work"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WORK_DIR, exist_ok=True)

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith(".mp4"):
            return
        path = event.src_path
        time.sleep(5)
        base = os.path.splitext(os.path.basename(path))[0]
        output_path = os.path.join(OUTPUT_DIR, f"{base}_4k.mp4")

        print(f"Detected new video: {path}")
        upscale(path, output_path, workdir=WORK_DIR)
        upload(output_path)

if __name__ == "__main__":
    print("Watching for new videos in:", INPUT_DIR)
    observer = Observer()
    observer.schedule(VideoHandler(), INPUT_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
