#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Drive Smart Sharing Engine
Tự động đồng bộ file PDF vào Google Drive Desktop và hỗ trợ lấy link chia sẻ công khai.
"""

import sys
import os
import shutil
import glob
import platform
import argparse
import subprocess

def find_local_google_drive_folder():
    """Tìm thư mục Google Drive for Desktop trên máy người dùng."""
    system = platform.system()
    home = os.path.expanduser("~")
    candidates = []
    
    if system == "Darwin": # macOS
        # Google Drive for Desktop thường nằm trong CloudStorage
        cloud_storage = os.path.join(home, "Library", "CloudStorage")
        if os.path.exists(cloud_storage):
            for d in os.listdir(cloud_storage):
                if d.startswith("GoogleDrive-") or "Google Drive" in d:
                    # Kiểm tra 'My Drive' hoặc 'Ổ đĩa của tôi'
                    drive_root = os.path.join(cloud_storage, d)
                    for sub in ["My Drive", "Ổ đĩa của tôi", "My_Drive"]:
                        sub_path = os.path.join(drive_root, sub)
                        if os.path.exists(sub_path):
                            candidates.append(sub_path)
                    candidates.append(drive_root)
        candidates.append(os.path.join(home, "Google Drive"))
        candidates.append(os.path.join(home, "GoogleDrive"))
        
    elif system == "Windows":
        # Windows thường có ổ đĩa G:, H: hoặc trong UserProfile
        for letter in ["G", "H", "I", "D", "E"]:
            candidates.append(f"{letter}:\\My Drive")
            candidates.append(f"{letter}:\\Ổ đĩa của tôi")
        candidates.append(os.path.join(home, "Google Drive"))
        candidates.append(os.path.join(home, "GoogleDrive"))
        
    for path in candidates:
        if os.path.exists(path) and os.path.isdir(path):
            return path
            
    return None

def sync_to_google_drive(pdf_file_path, folder_name="Phan_Tich_Video_FEDU"):
    """Sao chép file PDF vào Google Drive Desktop."""
    if not os.path.exists(pdf_file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {pdf_file_path}")
        
    drive_root = find_local_google_drive_folder()
    
    if drive_root:
        target_dir = os.path.join(drive_root, folder_name)
        os.makedirs(target_dir, exist_ok=True)
        file_name = os.path.basename(pdf_file_path)
        dest_path = os.path.join(target_dir, file_name)
        shutil.copy2(pdf_file_path, dest_path)
        print(f"☁️ ĐÃ ĐỒNG BỘ LÊN GOOGLE DRIVE DESKTOP!")
        print(f"📁 Vị trí trên Google Drive: {dest_path}")
        return {
            "status": "success",
            "type": "drive_desktop",
            "local_path": dest_path,
            "message": "File đã được tự động đồng bộ vào Google Drive của bạn."
        }
    else:
        print("💡 Chưa phát hiện Google Drive Desktop trên máy.")
        print(f"👉 File PDF đã sẵn sàng tại: {pdf_file_path}")
        return {
            "status": "local_only",
            "type": "local",
            "local_path": pdf_file_path,
            "message": "Bạn có thể kéo thả file PDF này trực tiếp vào drive.google.com để chia sẻ."
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Share PDF to Google Drive")
    parser.add_argument("pdf_path", help="Path to PDF report")
    parser.add_argument("--folder", default="Phan_Tich_Video_FEDU", help="Folder name in Drive")
    
    args = parser.parse_args()
    res = sync_to_google_drive(args.pdf_path, folder_name=args.folder)
    print(res["message"])
