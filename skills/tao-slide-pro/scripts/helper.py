#!/usr/bin/env python3
"""
Figma Live Sync Helper for Antigravity AI (On-Demand Mode)
Automates server health check, on-demand start, stop, selection retrieval, and command dispatch.
"""

import sys
import os
import json
import time
import urllib.request
import urllib.error
import subprocess

PORT = 8765
SERVER_URL = f"http://127.0.0.1:{PORT}"
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPT = os.path.join(SCRIPTS_DIR, "server.py")

def is_server_running():
    try:
        req = urllib.request.Request(f"{SERVER_URL}/api/selection")
        with urllib.request.urlopen(req, timeout=1) as resp:
            return resp.status == 200
    except Exception:
        return False

def start_server():
    if not is_server_running():
        subprocess.Popen(
            [sys.executable, SERVER_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        for _ in range(15):
            time.sleep(0.2)
            if is_server_running():
                break
    return is_server_running()

def stop_server():
    os.system(f"lsof -ti :{PORT} | xargs kill -9 2>/dev/null || true")
    time.sleep(0.3)
    return not is_server_running()

def ensure_server():
    if not is_server_running():
        start_server()

def get_selection():
    ensure_server()
    try:
        req = urllib.request.Request(f"{SERVER_URL}/api/selection")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        return {"status": "error", "message": str(e)}

def send_command(action, payload):
    ensure_server()
    try:
        body = json.dumps({"action": action, **payload}).encode("utf-8")
        req = urllib.request.Request(
            f"{SERVER_URL}/api/command",
            data=body,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        return {"status": "error", "message": f"HTTP {e.code}: {err_body}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: helper.py [start | stop | check | get | replace | update | create]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd == "start":
        ok = start_server()
        print(f'{{"status": "success", "server_running": {str(ok).lower()}}}')
    elif cmd == "stop":
        ok = stop_server()
        print(f'{{"status": "success", "server_stopped": {str(ok).lower()}}}')
    elif cmd == "check":
        running = is_server_running()
        print(f'{{"server_running": {str(running).lower()}}}')
    elif cmd == "get":
        res = get_selection()
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd == "replace":
        if len(sys.argv) < 3:
            print("Usage: helper.py replace <new_text>")
            sys.exit(1)
        res = send_command("REPLACE_SELECTION_TEXT", {"newText": sys.argv[2]})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd == "update":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("cmd")
        parser.add_argument("--title", default=None)
        parser.add_argument("--subtitle", default=None)
        parser.add_argument("--number", default=None)
        args = parser.parse_args()
        payload = {}
        if args.title: payload["title"] = args.title
        if args.subtitle: payload["subtitle"] = args.subtitle
        if args.number: payload["number"] = args.number
        res = send_command("UPDATE_SLIDE_TEXT", {"updates": payload})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd in ("clone", "clone_batch", "fast", "duplicate"):
        if len(sys.argv) < 3:
            print("Usage: helper.py clone '<slide_data_json_or_file>'")
            sys.exit(1)
        raw_arg = sys.argv[2]
        if os.path.isfile(raw_arg):
            with open(raw_arg, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.loads(raw_arg)
        
        if isinstance(data, list):
            res = send_command("CLONE_AND_SMART_FILL", {"slides": data})
        elif isinstance(data, dict) and "slides" in data:
            res = send_command("CLONE_AND_SMART_FILL", {"slides": data["slides"]})
        else:
            res = send_command("CLONE_AND_SMART_FILL", {"slideData": data})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd in ("create", "slides", "batch"):
        if len(sys.argv) < 3:
            print("Usage: helper.py create '<slide_json_or_file_path>'")
            sys.exit(1)
        raw_arg = sys.argv[2]
        if os.path.isfile(raw_arg):
            with open(raw_arg, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.loads(raw_arg)
        
        if isinstance(data, list):
            res = send_command("CREATE_SLIDES", {"slides": data})
        elif isinstance(data, dict) and "slides" in data:
            res = send_command("CREATE_SLIDES", {"slides": data["slides"]})
        else:
            res = send_command("CREATE_SLIDE", {"slideData": data})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd == "mindmap":
        if len(sys.argv) < 3:
            print("Usage: helper.py mindmap '<mindmap_json>'")
            sys.exit(1)
        data = json.loads(sys.argv[2])
        res = send_command("CREATE_FIGJAM_MINDMAP", {"mapData": data})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd == "stickies":
        if len(sys.argv) < 3:
            print("Usage: helper.py stickies '<stickies_json>'")
            sys.exit(1)
        data = json.loads(sys.argv[2])
        res = send_command("CREATE_FIGJAM_STICKIES", {"stickies": data})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd == "flow":
        if len(sys.argv) < 3:
            print("Usage: helper.py flow '<flow_steps_json>'")
            sys.exit(1)
        data = json.loads(sys.argv[2])
        res = send_command("CREATE_FIGJAM_FLOW", {"steps": data})
        print(json.dumps(res, ensure_ascii=False, indent=2))
    elif cmd in ("batch_replace", "translate"):
        if len(sys.argv) < 3:
            print("Usage: helper.py batch_replace '<json_dict_replacements>'")
            sys.exit(1)
        raw_arg = sys.argv[2]
        if os.path.isfile(raw_arg):
            with open(raw_arg, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.loads(raw_arg)
        res = send_command("BATCH_REPLACE_TEXTS", {"replacements": data})
        print(json.dumps(res, ensure_ascii=False, indent=2))
