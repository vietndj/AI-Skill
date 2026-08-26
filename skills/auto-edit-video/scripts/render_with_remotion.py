#!/usr/bin/env python3
"""
render_with_remotion.py — Bridge script that takes JSON config from Studio HTML
and calls Remotion CLI to render the final video.

Usage:
  python3 render_with_remotion.py --config config.json --video input.mp4 --output final.mp4
  
  Or pipe JSON from stdin:
  echo '{"scenes": [...]}' | python3 render_with_remotion.py --video input.mp4
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def find_remotion_dir():
    """Find the remotion-studio directory relative to this script."""
    script_dir = Path(__file__).parent.parent
    remotion_dir = script_dir / "remotion-studio"
    if remotion_dir.exists():
        return str(remotion_dir)
    # Fallback: check skill dir
    skill_dir = Path.home() / ".gemini" / "config" / "skills" / "auto-edit-video" / "remotion-studio"
    if skill_dir.exists():
        return str(skill_dir)
    raise FileNotFoundError("remotion-studio directory not found. Check installation.")


def prepare_assets(config: dict, video_path: str, remotion_dir: str) -> dict:
    """
    Copy video and image assets to remotion-studio/public/ so Remotion can access them.
    Returns updated config with staticFile-compatible paths.
    """
    public_dir = os.path.join(remotion_dir, "public")
    
    # Copy main video
    video_name = os.path.basename(video_path)
    dest_video = os.path.join(public_dir, video_name)
    if not os.path.exists(dest_video) or os.path.getmtime(video_path) > os.path.getmtime(dest_video):
        sys.stderr.write(f"Copying video to public/: {video_name}\n")
        shutil.copy2(video_path, dest_video)
    
    config["videoSrc"] = video_name
    
    # Copy scene images if they exist
    for scene in config.get("scenes", []):
        visual = scene.get("visual", {})
        if visual.get("type") == "image" and visual.get("file"):
            img_path = visual["file"]
            if os.path.exists(img_path):
                img_name = f"scene_{scene['scene']}_img{os.path.splitext(img_path)[1]}"
                dest_img = os.path.join(public_dir, img_name)
                shutil.copy2(img_path, dest_img)
                visual["file"] = img_name
                sys.stderr.write(f"  Copied image: {img_name}\n")
        
        if visual.get("type") == "broll" and visual.get("file"):
            broll_path = visual["file"]
            if os.path.exists(broll_path):
                broll_name = f"broll_{scene['scene']}{os.path.splitext(broll_path)[1]}"
                dest_broll = os.path.join(public_dir, broll_name)
                shutil.copy2(broll_path, dest_broll)
                visual["file"] = broll_name
                sys.stderr.write(f"  Copied B-roll: {broll_name}\n")
    
    return config


def calculate_duration_frames(config: dict, fps: int = 30) -> int:
    """Calculate total video duration in frames from scene configs."""
    max_end = 0
    for scene in config.get("scenes", []):
        end = scene.get("end", 0)
        if end > max_end:
            max_end = end
    # Add 1 second buffer
    return int((max_end + 1) * fps)


def render_video(config: dict, remotion_dir: str, output_path: str, 
                 composition_id: str = "AutoEditVideo", 
                 concurrency: int = 4,
                 codec: str = "h264",
                 crf: int = 18) -> bool:
    """
    Write inputProps JSON and call npx remotion render.
    """
    fps = 30
    duration_frames = calculate_duration_frames(config, fps)
    
    # Write props to temp file
    props_file = os.path.join(remotion_dir, "input-props.json")
    with open(props_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    sys.stderr.write(f"\n=== REMOTION RENDER ===\n")
    sys.stderr.write(f"Composition: {composition_id}\n")
    sys.stderr.write(f"Duration: {duration_frames} frames ({duration_frames/fps:.1f}s @ {fps}fps)\n")
    sys.stderr.write(f"Output: {output_path}\n")
    sys.stderr.write(f"Concurrency: {concurrency} threads\n")
    sys.stderr.write(f"Codec: {codec}, CRF: {crf}\n\n")
    
    cmd = [
        "npx", "remotion", "render",
        composition_id,
        output_path,
        f"--props={props_file}",
        f"--concurrency={concurrency}",
        f"--codec={codec}",
        f"--crf={crf}",
        "--pixel-format=yuv420p",
        "--gl=angle",
    ]
    
    sys.stderr.write(f"Running: {' '.join(cmd)}\n\n")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=remotion_dir,
            check=True,
            text=True,
        )
        sys.stderr.write(f"\n✅ Render complete: {output_path}\n")
        return True
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"\n❌ Render failed (exit code {e.returncode})\n")
        return False
    except FileNotFoundError:
        sys.stderr.write("❌ npx not found. Is Node.js installed?\n")
        return False


def render_overlay(config: dict, remotion_dir: str, output_path: str,
                   concurrency: int = 4) -> bool:
    """
    Render transparent overlay (ProRes 4444) for compositing in editors.
    """
    fps = 30
    duration_frames = calculate_duration_frames(config, fps)
    
    props_file = os.path.join(remotion_dir, "input-props.json")
    with open(props_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    cmd = [
        "npx", "remotion", "render",
        "MotionGraphicsOverlay",
        output_path,
        f"--props={props_file}",
        f"--concurrency={concurrency}",
        "--codec=prores",
        "--prores-profile=4444",
    ]
    
    sys.stderr.write(f"Rendering transparent overlay: {output_path}\n")
    
    try:
        subprocess.run(cmd, cwd=remotion_dir, check=True, text=True)
        sys.stderr.write(f"✅ Overlay render complete: {output_path}\n")
        return True
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"❌ Overlay render failed: {e}\n")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Render video using Remotion engine from Studio JSON config."
    )
    parser.add_argument("--config", help="Path to JSON config file (from Studio HTML export)")
    parser.add_argument("--video", required=True, help="Path to source video file")
    parser.add_argument("--output", help="Output video path (default: <video>_final.mp4)")
    parser.add_argument("--overlay", action="store_true", help="Also render transparent overlay (.mov)")
    parser.add_argument("--concurrency", type=int, default=4, help="Render threads (default: 4)")
    parser.add_argument("--codec", default="h264", choices=["h264", "h265", "vp8", "vp9", "prores"], help="Video codec")
    parser.add_argument("--crf", type=int, default=18, help="Quality (0-51, lower=better, default: 18)")
    parser.add_argument("--remotion-dir", help="Path to remotion-studio directory")
    
    args = parser.parse_args()
    
    # Read config from file or stdin
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        sys.stderr.write("Reading JSON config from stdin...\n")
        config = json.load(sys.stdin)
    
    # Find remotion directory
    remotion_dir = args.remotion_dir or find_remotion_dir()
    sys.stderr.write(f"Remotion dir: {remotion_dir}\n")
    
    # Prepare assets
    config = prepare_assets(config, args.video, remotion_dir)
    
    # Set output path
    video_name = os.path.splitext(os.path.basename(args.video))[0]
    output_path = args.output or f"{video_name}_final.mp4"
    output_path = os.path.abspath(output_path)
    
    # Render
    success = render_video(
        config, remotion_dir, output_path,
        concurrency=args.concurrency,
        codec=args.codec,
        crf=args.crf,
    )
    
    if success and args.overlay:
        overlay_path = output_path.replace(".mp4", "_overlay.mov")
        render_overlay(config, remotion_dir, overlay_path, concurrency=args.concurrency)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
