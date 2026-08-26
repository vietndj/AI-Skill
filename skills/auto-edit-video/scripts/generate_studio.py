#!/usr/bin/env python3
import os
import sys
import json
import base64
import argparse
import subprocess
import tempfile
import re
import shutil
from pathlib import Path

def parse_srt(filepath: str) -> list[dict]:
    """Parse a standard SRT file and return a list of dictionaries."""
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except Exception as e:
        sys.stderr.write(f"Error reading SRT file: {e}\n")
        return []

    # Simple SRT parser
    blocks = re.split(r'\n\s*\n', content.strip())
    subtitles = []
    
    def time_to_sec(time_str):
        # HH:MM:SS,mmm
        time_str = time_str.strip()
        parts = time_str.replace(',', '.').split(':')
        if len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        return 0.0

    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            index = int(lines[0].strip())
            times = lines[1].split('-->')
            if len(times) == 2:
                start = time_to_sec(times[0])
                end = time_to_sec(times[1])
                text = " ".join([line.strip() for line in lines[2:]])
                subtitles.append({
                    "index": index,
                    "start": start,
                    "end": end,
                    "text": text
                })
    return subtitles

def extract_frames(video_path: str, timestamps: list[float], output_dir: str) -> list[str]:
    """Use FFmpeg to extract frames at specific timestamps."""
    frame_paths = []
    
    if not shutil.which("ffmpeg"):
        sys.stderr.write("Error: ffmpeg is not installed or not in PATH.\n")
        return []

    for i, t in enumerate(timestamps):
        output_file = os.path.join(output_dir, f"frame_{i}.jpg")
        cmd = [
            "ffmpeg", "-y", "-ss", str(t), "-i", video_path, 
            "-vframes", "1", "-q:v", "2", output_file
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if os.path.exists(output_file):
                frame_paths.append(output_file)
            else:
                frame_paths.append(None)
        except subprocess.CalledProcessError:
            sys.stderr.write(f"Warning: Failed to extract frame at {t}s\n")
            frame_paths.append(None)
    
    return frame_paths

def image_to_base64(filepath: str) -> str:
    """Convert image file to data URI."""
    if not filepath or not os.path.exists(filepath):
        return ""
    try:
        ext = os.path.splitext(filepath)[1].lower()
        mime_type = "image/jpeg"
        if ext == ".png":
            mime_type = "image/png"
        elif ext in [".webp"]:
            mime_type = "image/webp"
            
        with open(filepath, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        sys.stderr.write(f"Error converting image to base64: {e}\n")
        return ""

def get_video_duration(video_path: str) -> float:
    """Use ffprobe to get video duration in seconds."""
    if not shutil.which("ffprobe"):
        sys.stderr.write("Error: ffprobe is not installed or not in PATH.\n")
        return 0.0

    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", video_path
    ]
    try:
        output = subprocess.check_output(cmd).decode('utf-8').strip()
        return float(output)
    except Exception as e:
        sys.stderr.write(f"Error getting video duration: {e}\n")
        return 0.0

def generate_studio_html(config: dict) -> str:
    """Generate the studio HTML by replacing variables in the template."""
    skill_dir = config['skill_dir']
    
    # 1. Read template (check resources/ first, then skill_dir root)
    template_path = os.path.join(skill_dir, "resources", "studio_template.html")
    if not os.path.exists(template_path):
        template_path = os.path.join(skill_dir, "studio_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        raise FileNotFoundError(f"Template not found. Checked:\n  - {os.path.join(skill_dir, 'resources', 'studio_template.html')}\n  - {os.path.join(skill_dir, 'studio_template.html')}\nError: {e}")

    # 2. Read DBs
    def find_resource(name):
        p1 = os.path.join(skill_dir, "resources", name)
        p2 = os.path.join(skill_dir, name)
        if os.path.exists(p1): return p1
        if os.path.exists(p2): return p2
        return None

    def read_json_file(name, fallback="[]"):
        path = find_resource(name)
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        sys.stderr.write(f"Warning: {name} not found, using fallback\n")
        return fallback
        
    styles_db = read_json_file("styles_db.json")
    presets_db = read_json_file("presets_db.json")

    # 3. Read fonts with proper font-family mapping
    # Map filename patterns to (font-family, weight, style)
    FONT_MAP = {
        'SVN-IntegralCF-Heavy': ('SVN-Integral', '900', 'normal'),
        'SVN-IntegralCF-Bold': ('SVN-Integral', '700', 'normal'),
        'SVN-AEONIK-BLACK': ('SVN-Aeonik', '900', 'normal'),
        'SVN-AEONIK-BOLD': ('SVN-Aeonik', '700', 'normal'),
        'SVN-AEONIK-REGULAR': ('SVN-Aeonik', '400', 'normal'),
        'GT-America-LCGV-Standard-Black': ('GT-America', '900', 'normal'),
        'GT-America-LCGV-Standard-Bold-Italic': ('GT-America', '700', 'italic'),
        'GT-America-LCGV-Standard-Bold': ('GT-America', '700', 'normal'),
        'GT-America-LCGV-Standard-Medium': ('GT-America', '500', 'normal'),
        'GT-Sectra-LCGV-Display-Bold-Italic': ('GT-Sectra', '700', 'italic'),
        'GT-Sectra-LCGV-Display-Bold': ('GT-Sectra', '700', 'normal'),
        'GT-Sectra-LCGV-Display-Super': ('GT-Sectra', '900', 'normal'),
        'GT-Sectra-LCGV-Display-Regular-Italic': ('GT-Sectra', '400', 'italic'),
        'SVN-FreightDisplay-BlackItalic': ('SVN-FreightDisplay', '900', 'italic'),
        'SVN-FreightDisplay-BoldItalic': ('SVN-FreightDisplay', '700', 'italic'),
        'SVN-FreightDisplay-MediumItalic': ('SVN-FreightDisplay', '500', 'italic'),
        'SVN-Flatline Bold Italic': ('SVN-Flatline', '700', 'italic'),
        'SVN-Flatline SemiBold Italic': ('SVN-Flatline', '600', 'italic'),
        'SVN-Flatline Regular Italic': ('SVN-Flatline', '400', 'italic'),
        'SVN-Acta-BoldItalic': ('SVN-Acta', '700', 'italic'),
        'SVN-Acta-MediumItalic': ('SVN-Acta', '500', 'italic'),
    }

    font_face_css = ""
    fonts_dir = os.path.join(skill_dir, "resources", "fonts")
    if not os.path.exists(fonts_dir):
        fonts_dir = os.path.join(skill_dir, "fonts")
    if os.path.exists(fonts_dir):
        for font_file in sorted(os.listdir(fonts_dir)):
            if font_file.lower().endswith(('.ttf', '.otf')):
                font_path = os.path.join(fonts_dir, font_file)
                font_stem = os.path.splitext(font_file)[0]
                mapping = FONT_MAP.get(font_stem)
                if not mapping:
                    continue  # Skip unmapped fonts
                family, weight, style = mapping
                try:
                    with open(font_path, 'rb') as f:
                        font_data = base64.b64encode(f.read()).decode('utf-8')
                    font_format = "truetype" if font_file.lower().endswith('.ttf') else "opentype"
                    mime_type = "font/ttf" if font_file.lower().endswith('.ttf') else "font/otf"
                    font_face_css += f"""@font-face {{ font-family: '{family}'; src: url('data:{mime_type};base64,{font_data}') format('{font_format}'); font-weight: {weight}; font-style: {style}; }}\n"""
                except Exception as e:
                    sys.stderr.write(f"Warning: Failed to load font {font_file}: {e}\n")

    # 4. Replace variables
    html = template
    html = html.replace("{{VIDEO_NAME}}", config['video_name'])
    html = html.replace("{{VIDEO_DURATION}}", str(config['video_duration']))
    html = html.replace("{{SCENE_COUNT}}", str(config['scene_count']))
    html = html.replace("{{SCENES_JSON}}", config['scenes_json'])
    html = html.replace("{{FRAME_IMAGES_JSON}}", config['frame_images_json'])
    html = html.replace("{{AI_IMAGES_JSON}}", config['ai_images_json'])
    html = html.replace("{{STYLES_DB_JSON}}", styles_db)
    html = html.replace("{{PRESETS_DB_JSON}}", presets_db)
    html = html.replace("{{FONT_FACE_CSS}}", font_face_css)
    html = html.replace("{{BRAND_LEFT}}", config['brand_left'])
    html = html.replace("{{BRAND_CENTER}}", config['brand_center'])
    html = html.replace("{{BRAND_RIGHT}}", config['brand_right'])

    return html

def main():
    parser = argparse.ArgumentParser(description="Generate Studio HTML for a video.")
    parser.add_argument("--video", required=True, help="Path to video file")
    parser.add_argument("--srt", required=True, help="Path to SRT file")
    parser.add_argument("--scenes", required=True, help="Path to scenes JSON")
    parser.add_argument("--images", help="Comma-separated paths to AI-generated images")
    parser.add_argument("--output", help="Output HTML path")
    parser.add_argument("--skill-dir", help="Path to skill directory")
    parser.add_argument("--brand-left", default="Viral Video COURSE")
    parser.add_argument("--brand-center", default="↗ 0934.68.86.32 (imess)")
    parser.add_argument("--brand-right", default="2026")
    
    args = parser.parse_args()

    # Set defaults
    video_path = args.video
    video_name = os.path.basename(video_path)
    output_path = args.output or f"studio_{os.path.splitext(video_name)[0]}.html"
    # Default skill_dir: look relative to this script's location
    if args.skill_dir:
        skill_dir = args.skill_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # If running from within auto-edit-tuquay/, resources are here
        if os.path.exists(os.path.join(script_dir, 'studio_template.html')):
            skill_dir = script_dir
        else:
            skill_dir = str(Path(script_dir).parent)

    sys.stderr.write(f"Processing video: {video_path}\n")

    # Parse SRT
    subtitles = parse_srt(args.srt)
    
    # Load Scenes
    try:
        with open(args.scenes, 'r', encoding='utf-8') as f:
            scenes = json.load(f)
    except Exception as e:
        sys.stderr.write(f"Error loading scenes JSON: {e}\n")
        sys.exit(1)

    # Enhance scenes with SRT text if needed (currently using scenes as-is)

    # Extract Frames
    scene_timestamps = [s.get('start', 0) for s in scenes]
    sys.stderr.write("Extracting frames...\n")
    with tempfile.TemporaryDirectory() as temp_dir:
        frame_paths = extract_frames(video_path, scene_timestamps, temp_dir)
        
        # Convert frames to Base64, keyed by scene number
        frame_images = {}
        for i, path in enumerate(frame_paths):
            if path and i < len(scenes):
                scene_num = str(scenes[i].get('scene', i + 1))
                frame_images[scene_num] = image_to_base64(path)
        
        # Convert AI images to Base64
        ai_images = {}
        if args.images:
            image_paths = [p.strip() for p in args.images.split(',')]
            for i, path in enumerate(image_paths):
                if i < len(scenes):
                    scene_num = str(scenes[i].get('scene', i + 1))
                    ai_images[scene_num] = image_to_base64(path)

        # Get duration
        video_duration = get_video_duration(video_path)

        # Build Config
        config = {
            'skill_dir': skill_dir,
            'video_name': video_name,
            'video_duration': video_duration,
            'scene_count': len(scenes),
            'scenes_json': json.dumps(scenes, ensure_ascii=False),
            'frame_images_json': json.dumps(frame_images, ensure_ascii=False),
            'ai_images_json': json.dumps(ai_images, ensure_ascii=False),
            'brand_left': args.brand_left,
            'brand_center': args.brand_center,
            'brand_right': args.brand_right
        }

        # Generate HTML
        sys.stderr.write("Generating HTML...\n")
        try:
            html = generate_studio_html(config)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            sys.stderr.write(f"Success! Studio HTML saved to {output_path}\n")
        except Exception as e:
            sys.stderr.write(f"Error generating HTML: {e}\n")
            sys.exit(1)

if __name__ == "__main__":
    main()
