#!/usr/bin/env python3
"""
Figma Live Sync Bridge Server (VietMac AI Studio)
Provides real-time 2-way communication between Figma Desktop and Antigravity AI.
"""

import asyncio
import json
import os
import sys
import time
from aiohttp import web
import aiohttp_cors

PORT = 8765
BASE_DIR = "/Users/vietmac/Documents/CODE/Quản gia/figma-live-sync"
os.makedirs(BASE_DIR, exist_ok=True)

STATE_FILE = os.path.join(BASE_DIR, "current_selection.json")
LOG_FILE = os.path.join(BASE_DIR, "bridge.log")

connected_websockets = set()
latest_selection = {"timestamp": 0, "selection": []}
latest_deck_info = {"timestamp": 0, "slides": []}

def log(msg):
    t = time.strftime("%H:%M:%S")
    line = f"[{t}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected_websockets.add(ws)
    log(f"🟢 Figma Plugin connected (Total clients: {len(connected_websockets)})")

    # Send welcome / ping
    await ws.send_json({"type": "INIT_ACK", "message": "Connected to Viet AI Bridge Server"})

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    event_type = data.get("event") or data.get("type")

                    if event_type == "SELECTION_CHANGED":
                        payload = data.get("payload", data.get("data", {}))
                        global latest_selection
                        latest_selection = {
                            "timestamp": time.time(),
                            "human_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "data": payload.get("data", payload) if isinstance(payload, dict) else payload,
                            "deck": payload.get("deck", []) if isinstance(payload, dict) else [],
                            "viewport": payload.get("viewport", {}) if isinstance(payload, dict) else {}
                        }
                        with open(STATE_FILE, "w", encoding="utf-8") as f:
                            json.dump(latest_selection, f, ensure_ascii=False, indent=2)

                        sel_data = latest_selection["data"]
                        summary = []
                        if isinstance(sel_data, list):
                            for item in sel_data:
                                if item.get("type") == "TEXT":
                                    summary.append(f'TEXT: "{item.get("characters", "")}"')
                                elif item.get("texts"):
                                    txts = [f'"{t.get("characters")}"' for t in item.get("texts", [])[:3]]
                                    summary.append(f'{item.get("type")} "{item.get("name")}": [{", ".join(txts)}]')
                                else:
                                    summary.append(f'{item.get("type")} "{item.get("name")}"')
                        log(f"📍 Selection updated: {'; '.join(summary) if summary else 'Empty selection'}")

                    elif event_type == "DECK_INFO":
                        payload = data.get("payload", [])
                        global latest_deck_info
                        latest_deck_info = {
                            "timestamp": time.time(),
                            "human_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "slides": payload
                        }
                        with open(os.path.join(BASE_DIR, "deck_info.json"), "w", encoding="utf-8") as f:
                            json.dump(latest_deck_info, f, ensure_ascii=False, indent=2)
                        log(f"📚 Deck info updated: {len(payload)} slides")

                    elif event_type == "EVAL_RESULT":
                        payload = data.get("payload")
                        log(f"📋 EVAL Result: {str(payload)[:200]}")
                        with open("/tmp/eval_result.json", "w", encoding="utf-8") as f:
                            json.dump({"result": payload, "timestamp": time.time()}, f, ensure_ascii=False, indent=2)

                    elif event_type == "PONG":
                        pass
                except Exception as e:
                    log(f"❌ Error parsing WS message: {e}")
            elif msg.type == web.WSMsgType.ERROR:
                log(f"⚠️ WS error: {ws.exception()}")
    finally:
        connected_websockets.discard(ws)
        log(f"🔴 Figma Plugin disconnected (Remaining clients: {len(connected_websockets)})")

    return ws

async def get_deck_handler(request):
    return web.json_response({
        "status": "success",
        "deck": latest_deck_info
    })

async def get_selection_handler(request):
    return web.json_response({
        "status": "success",
        "clients_count": len(connected_websockets),
        "selection": latest_selection
    })

async def send_command_handler(request):
    try:
        body = await request.json()
        if not connected_websockets:
            return web.json_response({
                "status": "error",
                "message": "Không có client Figma nào đang kết nối! Hãy mở plugin trong Figma."
            }, status=400)

        dead_ws = set()
        for ws in list(connected_websockets):
            try:
                if not ws.closed:
                    await ws.send_json(body)
                else:
                    dead_ws.add(ws)
            except Exception:
                dead_ws.add(ws)

        connected_websockets.difference_update(dead_ws)
        log(f"⚡ Dispatched command to {len(connected_websockets)} Figma client(s): {body.get('action')}")
        return web.json_response({
            "status": "success",
            "sent_to_clients": len(connected_websockets),
            "command": body
        })
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        log(f"❌ Error dispatching command: {tb}")
        return web.json_response({"status": "error", "message": str(e), "traceback": tb}, status=500)

def init_app():
    app = web.Application()
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })

    app.router.add_get("/ws", websocket_handler)

    r_sel = app.router.add_get("/api/selection", get_selection_handler)
    r_deck = app.router.add_get("/api/deck", get_deck_handler)
    r_cmd = app.router.add_post("/api/command", send_command_handler)

    cors.add(r_sel)
    cors.add(r_deck)
    cors.add(r_cmd)

    return app

if __name__ == "__main__":
    app = init_app()
    log(f"🚀 VietMac Live Bridge Server starting on http://127.0.0.1:{PORT}")
    web.run_app(app, host="127.0.0.1", port=PORT, print=None)
