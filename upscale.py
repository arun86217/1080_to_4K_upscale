import os, math, time, subprocess, multiprocessing as mp, glob, json
from datetime import timedelta
from tqdm import tqdm

def get_duration(file):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","default=noprint_wrappers=1:nokey=1",file],
                        capture_output=True,text=True)
    return float(r.stdout.strip())

def get_resolution(file):
    r = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
                        "-show_entries","stream=width,height",
                        "-of","csv=p=0",file],
                        capture_output=True,text=True)
    return map(int, r.stdout.strip().split(','))

def upscale(input_file, output_file, workdir="work", segment_duration=120):
    os.makedirs(workdir, exist_ok=True)
    resume_log = os.path.join(workdir, "resume_log.json")

    total_duration = get_duration(input_file)
    num_segments = math.ceil(total_duration / segment_duration)
    segments = [
        (i * segment_duration, min(segment_duration, total_duration - i * segment_duration), i)
        for i in range(num_segments)
    ]

    # resume detection
    completed = set()
    if os.path.exists(resume_log):
        try:
            with open(resume_log, "r") as f:
                completed = set(json.load(f))
        except: pass

    print(f"🎬 Upscaling started\n➡️ {input_file} → {output_file}")
    print(f"Segments: {num_segments}, Resume from {len(completed)}/{num_segments}")

    def upscale_segment(start, dur, idx):
        seg_out = os.path.join(workdir, f"seg_{idx:03d}.mp4")
        if idx in completed and os.path.exists(seg_out):
            return seg_out, 0  # already done

        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", str(start), "-t", str(dur),
            "-i", input_file,
            "-vf", "scale=3840:2160:flags=lanczos,unsharp=5:5:1.2",
            "-c:v", "h264_qsv", "-pix_fmt", "yuv420p",
            "-b:v", "35M", "-maxrate", "45M", "-bufsize", "70M",
            "-preset", "7", "-look_ahead", "1",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            seg_out
        ]
        start_t = time.time()
        subprocess.run(cmd)
        duration = time.time() - start_t

        completed.add(idx)
        with open(resume_log, "w") as f:
            json.dump(list(completed), f)
        return seg_out, duration

    # parallel execution with tqdm
    results = []
    start_time = time.time()
    with mp.Pool(max(1, mp.cpu_count()-2)) as pool, tqdm(total=num_segments, desc="Upscaling", ncols=80) as pbar:
        for seg in segments:
            seg_start, seg_dur, seg_idx = seg
            if seg_idx in completed:
                pbar.update(1)
                continue
            res = pool.apply_async(upscale_segment, seg, callback=lambda _: pbar.update(1))
            results.append(res)
        pool.close()
        pool.join()

    # concatenate
    seg_files = [os.path.join(workdir, f"seg_{i:03d}.mp4") for i in range(num_segments) if os.path.exists(os.path.join(workdir, f"seg_{i:03d}.mp4"))]
    with open(os.path.join(workdir, "concat.txt"), "w") as f:
        for s in seg_files:
            f.write(f"file '{s}'\n")

    print("\n🔗 Merging segments…")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i",
                    os.path.join(workdir, "concat.txt"), "-c", "copy", output_file])

    # cleanup
    for f in seg_files + [os.path.join(workdir, "concat.txt"), resume_log]:
        try: os.remove(f)
        except: pass
    print(f"\n✅ Done! Total time {timedelta(seconds=int(time.time()-start_time))}")
    print(f"Output → {output_file}")
