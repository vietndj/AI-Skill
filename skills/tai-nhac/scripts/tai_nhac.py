#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kỹ Năng Tải Nhạc Đa Nền Tảng & Đồng Bộ Tự Động (TAI NHAC SKILL)
Tác giả: NOVA-CORE / Antigravity Quản Gia

Quy trình tự động 4 bước:
1. Nhận diện URL (Instagram Audio/Reels, YouTube, TikTok, SoundCloud,...) hoặc tên bài hát.
   - Tự động bóc tách tên bài hát & nghệ sĩ từ link Instagram audio/reels.
   - Tìm kiếm bài hát gốc bản Master Full (Official Audio / Studio Version 320kbps).
   - Tải về và convert sang chuẩn MP3 chất lượng cao nhất tại ~/Documents/Nhạc tai ve/
2. Tự động đồng bộ lên Google Drive của anh Việt (gdrive:Nhạc tai ve).
3. Lấy link chia sẻ Google Drive trực tiếp.
4. Gửi file MP3 trực tiếp (Telegram Music Player) + Caption chi tiết qua Bot NOVA-CORE (@nova0410_bot).
"""

import os
import sys
import re
import json
import ssl
import subprocess
import urllib.request
import argparse
from pathlib import Path

LOCAL_DIR = Path("/Users/vietmac/Documents/Nhạc tai ve")
GDRIVE_REMOTE_DIR = "gdrive:Nhạc tai ve"
TELEGRAM_SCRIPT = Path("/Users/vietmac/Documents/CODE/Quản gia/telegram_notify.py")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def resolve_instagram_audio(url: str) -> dict:
    """Trích xuất thông tin bài hát từ mọi dạng link Instagram (audio, reels, posts)"""
    headers = {
        "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    # Loại bỏ query params thừa
    clean_url = url.split("?")[0].rstrip("/") + "/"
    artist = ""
    title = ""
    
    try:
        req = urllib.request.Request(clean_url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        # 1. Tìm og:title
        og_title_m = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', html, re.I)
        raw_title = og_title_m.group(1) if og_title_m else ""
        
        # 2. Tìm og:description
        og_desc_m = re.search(r'<meta\s+(?:property=["\']og:description["\']|content=["\'](.*?)["\']\s+name=["\']description["\'])', html, re.I)
        raw_desc = ""
        if og_desc_m:
            raw_desc = og_desc_m.group(1) or ""
        if not raw_desc:
            desc_m = re.search(r'name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
            if desc_m:
                raw_desc = desc_m.group(1)
        
        if not raw_title:
            title_m = re.search(r"<title>(.*?)</title>", html, re.I)
            raw_title = title_m.group(1) if title_m else ""
            
        if raw_title:
            # Xóa hậu tố rác của Instagram
            cleaned = re.sub(r"\s+on Instagram.*", "", raw_title, flags=re.I)
            cleaned = re.sub(r"\s+•\s+Instagram.*", "", cleaned, flags=re.I)
            cleaned = re.sub(r"\s+\|\s+Instagram.*", "", cleaned, flags=re.I)
            cleaned = re.sub(r"^Instagram\s+audio\s+by\s+", "", cleaned, flags=re.I).strip()
            
            # Phân tách Artist | Title hoặc Artist · Title hoặc Artist - Title
            if " | " in cleaned:
                parts = cleaned.split(" | ", 1)
                artist = parts[0].strip()
                title = parts[1].strip()
            elif " · " in cleaned:
                parts = cleaned.split(" · ", 1)
                artist = parts[0].strip()
                title = parts[1].strip()
            elif " - " in cleaned:
                parts = cleaned.split(" - ", 1)
                artist = parts[0].strip()
                title = parts[1].strip()
            else:
                title = cleaned
                
        # Nếu vẫn thiếu artist hoặc title, phân tích description: "Listen to <Artist> on Instagram and watch reels using <Title> audio"
        if raw_desc and (not artist or not title or title.lower() == "instagram"):
            desc_match = re.search(r"Listen to (.*?) on Instagram and watch reels using (.*?) audio", raw_desc, re.I)
            if desc_match:
                artist = desc_match.group(1).strip()
                title = desc_match.group(2).strip()

    except Exception as e:
        print(f"[Info] HTML parse Instagram: {e}", file=sys.stderr)

    # Cách 2: Nếu chưa tìm được thông tin, thử dùng yt-dlp dump-json trực tiếp
    if not title or title.lower() in ["instagram", "instagram audio", ""]:
        try:
            cmd = ["yt-dlp", "--dump-json", "--no-playlist", clean_url]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
            if proc.returncode == 0 and proc.stdout.strip():
                data = json.loads(proc.stdout.strip().splitlines()[0])
                track = data.get("track")
                art = data.get("artist") or data.get("creator") or data.get("uploader")
                t = data.get("title")
                if track:
                    title = track
                    artist = art or artist
                elif t:
                    title = t
                    artist = art or artist
        except Exception:
            pass

    search_query = f"{artist} {title}".strip() if (artist and title) else (title or "Instagram Audio")
    
    return {
        "is_ig_audio": True,
        "title": title or "Instagram Audio",
        "artist": artist,
        "search_query": search_query,
        "original_url": url
    }

def find_best_audio_match(query: str, artist: str = "", title: str = "") -> str:
    """Tìm bản phát hành gốc Master Full (Official Audio / Video) khớp nhất trên YouTube"""
    clean_artist = artist.lower().strip() if artist else ""
    clean_title = title.lower().strip() if title else ""
    
    enhanced_query = query
    if not any(k in query.lower() for k in ["official", "audio", "full"]):
        enhanced_query = f"{query} official audio full"
        
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--default-search", "ytsearch10",
        "--no-playlist",
        enhanced_query
    ]
    
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    best_id = None
    best_score = -9999
    best_title = ""

    for line in proc.stdout.splitlines():
        if line.startswith("{") and line.endswith("}"):
            try:
                item = json.loads(line)
                it_title = item.get("title", "").lower()
                it_uploader = item.get("uploader", "").lower()
                it_channel = item.get("channel", "").lower()
                it_duration = item.get("duration", 0) or 0
                it_id = item.get("id")
                
                score = 0
                
                # 1. Khớp nghệ sĩ
                if clean_artist:
                    if clean_artist in it_uploader or clean_artist in it_channel:
                        score += 80
                    elif clean_artist in it_title:
                        score += 50
                        
                # 2. Khớp tên bài
                if clean_title:
                    if clean_title in it_title:
                        score += 70
                        
                # 3. Ưu tiên bài phát hành chính thức (Official, Topic, VEVO, Full Audio)
                if "topic" in it_uploader or "topic" in it_channel or "vevo" in it_uploader:
                    score += 60
                if "official audio" in it_title:
                    score += 50
                elif "official music video" in it_title or "official video" in it_title:
                    score += 40
                elif "audio" in it_title or "full audio" in it_title:
                    score += 30
                    
                # 4. Tiêu chí thời lượng (Tránh clip ngắn/Reels/Shorts, ưu tiên bài hát đầy đủ 1.5 - 7 phút)
                if it_duration >= 90 and it_duration <= 420:
                    score += 40
                elif it_duration > 420 and it_duration <= 600:
                    score += 10
                elif it_duration < 45:
                    score -= 150  # Phạt nặng video ngắn / Shorts / Reels bị cắt
                elif it_duration > 900:
                    score -= 100  # Phạt video tổng hợp 1 tiếng / loop

                # 5. Phạt các bản remix / speed up / slowed / 8D nếu không được yêu cầu
                penalty_words = ["sped up", "speed up", "slowed", "nightcore", "8d audio", "bass boosted", "1 hour", "10 hours", "tiktok version"]
                for p in penalty_words:
                    if p in it_title and p not in query.lower():
                        score -= 80

                if score > best_score:
                    best_score = score
                    best_id = it_id
                    best_title = item.get("title", "")
            except Exception:
                pass

    if best_id:
        print(f"🎯 Đã chọn bản gốc Master phù hợp nhất: '{best_title}' (Score: {best_score})")
        return f"https://www.youtube.com/watch?v={best_id}"
        
    return query

def download_audio(target: str, output_dir: Path) -> dict:
    """Tải và convert sang MP3 320kbps vào output_dir"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    is_ig = any(domain in target.lower() for domain in ["instagram.com/reels/audio", "instagram.com/audio", "instagram.com/reel", "instagram.com/p"])
    
    song_info = {}
    if is_ig:
        print(f"🔍 Đang phân tích link âm thanh Instagram: {target}")
        song_info = resolve_instagram_audio(target)
        query = song_info["search_query"]
        print(f"🎵 Đã nhận diện: {song_info['artist']} - {song_info['title']} (Query: '{query}')")
        
        # Tìm bản nhạc gốc đầy đủ trên YouTube
        download_target = find_best_audio_match(query, artist=song_info["artist"], title=song_info["title"])
    else:
        download_target = target

    outtmpl = str(output_dir / "%(title)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--extractor-args", "youtube:player_client=ios,android",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--embed-metadata",
        "--no-playlist",
        "-o", outtmpl,
        "--print-json",
        download_target
    ]

    print(f"🚀 Đang tải và trích xuất MP3 320kbps Master...")
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if proc.returncode != 0:
        print(f"⚠️ Thử chế độ fallback tải audio...")
        cmd_fallback = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-metadata",
            "--no-playlist",
            "-o", outtmpl,
            "--print-json",
            download_target
        ]
        proc = subprocess.run(cmd_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if proc.returncode != 0:
        raise RuntimeError(f"Lỗi khi tải audio: {proc.stderr.strip()}")

    meta = {}
    for line in proc.stdout.splitlines():
        if line.startswith("{") and line.endswith("}"):
            try:
                meta = json.loads(line)
                break
            except Exception:
                pass
    
    mp3_files = sorted(output_dir.glob("*.mp3"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not mp3_files:
        raise FileNotFoundError("Không tìm thấy file .mp3 nào sau khi tải!")
    
    target_file = mp3_files[0]
    file_size_mb = target_file.stat().st_size / (1024 * 1024)
    
    final_title = meta.get("title") or song_info.get("title") or target_file.stem
    final_artist = meta.get("artist") or meta.get("uploader") or song_info.get("artist") or ""
    
    return {
        "file_path": str(target_file),
        "file_name": target_file.name,
        "file_size_mb": round(file_size_mb, 2),
        "title": final_title,
        "artist": final_artist,
        "duration": meta.get("duration_string", "N/A"),
        "source_url": meta.get("webpage_url", download_target)
    }

def upload_to_gdrive(local_file: str, remote_dir: str) -> str:
    """Upload file lên Google Drive và lấy link chia sẻ trực tiếp"""
    file_name = Path(local_file).name
    print(f"☁️ Đang upload '{file_name}' lên Google Drive ({remote_dir})...")
    
    cmd_upload = ["rclone", "copy", local_file, remote_dir, "-v"]
    proc_up = subprocess.run(cmd_upload, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc_up.returncode != 0:
        raise RuntimeError(f"Lỗi upload Drive: {proc_up.stderr.strip()}")

    remote_file_path = f"{remote_dir}/{file_name}"
    cmd_link = ["rclone", "link", remote_file_path]
    proc_link = subprocess.run(cmd_link, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    drive_link = proc_link.stdout.strip()
    if not drive_link or "http" not in drive_link:
        cmd_folder_link = ["rclone", "link", remote_dir]
        proc_f = subprocess.run(cmd_folder_link, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        drive_link = proc_f.stdout.strip()

    return drive_link

def send_telegram_music(audio_info: dict, drive_link: str):
    """Gửi trực tiếp file MP3 với Telegram Music Player và caption đầy đủ qua NOVA Bot"""
    if not TELEGRAM_SCRIPT.exists():
        print(f"[Cảnh báo] Không tìm thấy telegram_notify.py tại {TELEGRAM_SCRIPT}", file=sys.stderr)
        return

    title = audio_info["title"]
    artist = audio_info["artist"]
    duration = audio_info["duration"]
    size_mb = audio_info["file_size_mb"]
    file_name = audio_info["file_name"]
    file_path = audio_info["file_path"]

    caption = (
        f"🎧 <b>{title}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Nghệ sĩ:</b> {artist or 'N/A'}\n"
        f"⏱ <b>Thời lượng:</b> {duration}\n"
        f"📦 <b>Dung lượng:</b> {size_mb} MB (MP3 320kbps Master)\n"
        f"📂 <b>File máy:</b> <code>{file_name}</code>\n"
        f"🔗 <b>Google Drive:</b> {drive_link}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"✨ Đã đồng bộ vào thư mục 'Nhạc tai ve' trên máy & Drive của anh Việt!"
    )

    # Gửi file audio trực tiếp để nghe ngay trên Telegram
    cmd_audio = [
        "python3", str(TELEGRAM_SCRIPT),
        "--audio", file_path,
        "--title", title,
        "--performer", artist or "NOVA Music",
        "--caption", caption
    ]
    
    print(f"📲 Đang gửi file MP3 trực tiếp sang Telegram (@nova0410_bot)...")
    proc = subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode == 0:
        print("✅ Đã gửi file nhạc MP3 sang Telegram thành công!")
    else:
        print(f"⚠️ Gửi audio lỗi ({proc.stderr.strip()}), fallback gửi tin nhắn văn bản...")
        cmd_msg = ["python3", str(TELEGRAM_SCRIPT), "--msg", caption]
        subprocess.run(cmd_msg)

def main():
    parser = argparse.ArgumentParser(description="Tự động tải nhạc Master từ Instagram/YouTube/TikTok, đồng bộ Drive và gửi Telegram")
    parser.add_argument("target", help="URL video/audio hoặc tên bài hát cần tải")
    parser.add_argument("--no-telegram", action="store_true", help="Không gửi Telegram")
    parser.add_argument("--no-drive", action="store_true", help="Không upload Google Drive")
    args = parser.parse_args()

    try:
        print(f"🎵 BẮT ĐẦU TIẾN TRÌNH TẢI NHẠC: {args.target}")
        
        audio_info = download_audio(args.target, LOCAL_DIR)
        print(f"✅ Đã tải về máy: {audio_info['file_path']} ({audio_info['file_size_mb']} MB)")

        drive_link = ""
        if not args.no_drive:
            drive_link = upload_to_gdrive(audio_info["file_path"], GDRIVE_REMOTE_DIR)
            print(f"✅ Link Google Drive: {drive_link}")

        if not args.no_telegram:
            send_telegram_music(audio_info, drive_link)

        print("\n🎉 TOÀN BỘ QUY TRÌNH ĐÃ HOÀN TẤT XUẤT SẮC!")
        print(json.dumps({
            "status": "success",
            "file_path": audio_info["file_path"],
            "file_name": audio_info["file_name"],
            "size_mb": audio_info["file_size_mb"],
            "title": audio_info["title"],
            "artist": audio_info["artist"],
            "duration": audio_info["duration"],
            "drive_link": drive_link
        }, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"\n❌ LỖI: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

