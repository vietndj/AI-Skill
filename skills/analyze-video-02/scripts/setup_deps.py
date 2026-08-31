#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Dependencies for Video Analysis 02 (Director's Shot Notebook)
Tự động kiểm tra và cài đặt ngầm toàn bộ thư viện cần thiết.
"""

import sys
import subprocess
import importlib.util
import os
import platform

REQUIRED_PACKAGES = {
    "yt_dlp": "yt-dlp",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "googleapiclient": "google-api-python-client",
    "google_auth_oauthlib": "google-auth-oauthlib",
}

def is_package_installed(package_name):
    return importlib.util.find_spec(package_name) is not None

def install_package(pip_name):
    print(f"📦 Đang tự động cài đặt thư viện: {pip_name}...")
    try:
        cmd = [sys.executable, "-m", "pip", "install", pip_name, "--quiet"]
        subprocess.check_call(cmd)
        print(f"✅ Đã cài đặt thành công: {pip_name}")
        return True
    except Exception as e:
        print(f"⚠️ Không thể tự cài {pip_name}: {e}")
        return False

def check_and_install_all():
    missing = []
    for module_name, pip_name in REQUIRED_PACKAGES.items():
        if not is_package_installed(module_name):
            missing.append(pip_name)
    
    if not missing:
        print("✅ Toàn bộ thư viện Python đã sẵn sàng 100%!")
        return True
    
    print(f"🔍 Phát hiện {len(missing)} thư viện cần cài đặt: {', '.join(missing)}")
    for pip_name in missing:
        install_package(pip_name)
    
    return True

def find_chrome_executable():
    """Tìm đường dẫn Google Chrome / Chromium trên máy để in PDF."""
    system = platform.system()
    candidates = []
    
    if system == "Darwin": # macOS
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    elif system == "Windows":
        candidates = [
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
            os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
        ]
    else: # Linux
        candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
        ]
        
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

if __name__ == "__main__":
    check_and_install_all()
    chrome_path = find_chrome_executable()
    if chrome_path:
        print(f"✅ Đã tìm thấy trình duyệt để xuất PDF: {chrome_path}")
    else:
        print("⚠️ Chưa tìm thấy Google Chrome/Edge. Vui lòng cài Google Chrome để xuất file PDF đẹp nhất.")
