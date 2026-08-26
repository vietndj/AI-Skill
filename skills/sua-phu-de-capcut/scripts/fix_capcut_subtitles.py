#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CÔNG CỤ SỬA PHỤ ĐỀ CAPCUT PC TỰ ĐỘNG - PHIÊN BẢN V5 (MULTI-LEVEL FILTER & SMART 2-LINE BREAK)
Tự động quét dự án CapCut mới nhất, lọc sạch từ đệm thừa ("ấy", "ý", "một cái", "để mà"...),
ngắt 2 dòng cân bằng chống xé chữ trên video 9:16 và đồng bộ token 1-to-1.
"""

import sys
import os
import json
import re
import argparse
import time
import shutil

def get_latest_project():
    capcut_dir = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
    projects = []
    if not os.path.exists(capcut_dir):
        return None, None
    for item in os.listdir(capcut_dir):
        p_path = os.path.join(capcut_dir, item)
        if os.path.isdir(p_path) and not item.startswith('.'):
            draft_file = os.path.join(p_path, 'draft_info.json')
            if os.path.exists(draft_file):
                mtime = os.path.getmtime(draft_file)
                projects.append((mtime, item, p_path))
    if not projects:
        return None, None
    projects.sort(reverse=True)
    return projects[0][1], projects[0][2]

def clean_vietnamese_subtitles(text, level=2):
    """
    3 Chế độ lọc từ thừa:
    - Level 1: Lọc từ đệm cơ bản (ờ, à, ừm, ấy, ý, nhé, nè, từ lặp)
    - Level 2 (Default): Lọc cô đọng Short-form (bỏ một cái, những cái, để mà, sau khi mà, cho nên là, rất là, xong rồi...)
    - Level 3: Siêu cô đọng / Action-driven
    """
    if not text or not isinstance(text, str):
        return text

    # --- LEVEL 1: TỪ ĐỆM CƠ BẢN & TỪ LẶP ---
    fillers_l1 = [
        r'(ờ|ừm|ừ|hả|hờ|à|nè|nhé|nhỉ|nha)',
        r'kiểu như',
        r'thì là',
        r'ý là',
        r'kiểu kiểu',
        r'dạng như',
        r'việc à',
        r'luôn ấy',
        r'ấy(?=[,\.\s
]|$)',
        r'ý(?=[,\.\s
]|$)(?<!chú )(?<!ý )'
    ]
    for pattern in fillers_l1:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Xóa từ lặp vô nghĩa (vd: "tôi tôi", "là là", "và và", "sẽ a sẽ")
    text = re.sub(r'sẽ\s+a\s+sẽ', 'sẽ', text, flags=re.IGNORECASE)
    text = re.sub(r'(\w+)\s+', r'', text, flags=re.IGNORECASE)

    # Lọc đuôi liệt kê "này"
    text = re.sub(r'(này|nè)(?=[,\.\s
]|$)', ',', text, flags=re.IGNORECASE)

    # --- LEVEL 2: LỌC TỪ NỐI RƯỜM RÀ & CÔ ĐỌNG SHORT-FORM ---
    if level >= 2:
        fillers_l2 = [
            (r'một cái', 'một'),
            (r'những cái', 'những'),
            (r'các cái', 'các'),
            (r'để mà', 'để'),
            (r'sau khi mà', 'sau khi'),
            (r'cho nên là', 'nên'),
            (r'bởi vì là', 'vì'),
            (r'cho nên', 'nên'),
            (r'bởi vì', 'vì'),
            (r'rất là', 'rất'),
            (r'xong rồi', ''),
            (r'nói chung là', ''),
            (r'tức là', ''),
            (r'ấy thì', 'thì'),
            (r'thế là mình phải', 'thế là phải'),
            (r'mình có thể', 'có thể'),
        ]
        for pattern, repl in fillers_l2:
            text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # --- LEVEL 3: SIÊU CÔ ĐỌNG / ACTION-DRIVEN ---
    if level >= 3:
        fillers_l3 = [
            (r'chúng ta', ''),
            (r'bạn có thể', ''),
            (r'chỉ là', 'chỉ'),
            (r'có nghĩa là', ''),
        ]
        for pattern, repl in fillers_l3:
            text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # Chuẩn hóa khoảng trắng & dấu câu thừa
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r',\s*,+', ',', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'^[,.\s]+', '', text)
    text = re.sub(r'[,.\s]+$', '', text)

    # Chuẩn hóa tên thương hiệu & thuật ngữ
    typo_map = {
        r'chat gpt': 'ChatGPT',
        r'chatgpt': 'ChatGPT',
        r'youtube': 'YouTube',
        r'tiktok': 'TikTok',
        r'facebook': 'Facebook',
        r'app store': 'App Store',
        r'play store': 'Play Store',
        r'ch play': 'CH Play',
        r'capcut': 'CapCut',
        r'capcut pc': 'CapCut PC',
        r'broll': 'B-roll',
        r'cutaway': 'Cutaway',
        r'talking head': 'Talking Head',
        r'video ask': 'video Ads',
        r'video ads': 'Video Ads',
        r'video marketing': 'Video Marketing',
        r'đế chế': 'Đế Chế',
        r'game đế chế': 'game Đế Chế',
        r'mua bông đồng': 'mua bốc đồng',
        r'quay học': 'quay hỏng',
    }
    for k, v in typo_map.items():
        text = re.sub(k, v, text, flags=re.IGNORECASE)

    # Sửa lỗi viết hoa tùy tiện của CapCut Auto-Caption
    proper_nouns = {'AI', 'TV', 'Grab', 'Hà', 'Nội', 'Vincom', 'CapCut', 'Google', 'Python', 'YouTube', 'TikTok', 'Facebook', 'ChatGPT', 'App', 'Store', 'Play', 'CH', 'B-roll', 'Cutaway', 'Talking', 'Head', 'Ads', 'Video', 'Marketing', 'Đế', 'Chế'}
    capcut_bad_caps = {
        'Cho', 'Sao', 'Ra', 'Sai', 'Theo', 'Chung', 'Ba', 'Hóa', 'Chi', 'Nó', 'Tức', 'Bởi', 
        'Và', 'Nhưng', 'Thì', 'Có', 'Từ', 'Trên', 'Trong', 'Đó', 'Thấy', 'Cho nên', 'Bởi vì', 
        'Nên', 'Là', 'Về', 'Để', 'Của', 'Được', 'Khi', 'Nếu', 'Thực', 'Nơi', 'Đấy', 'Ấy', 'Hơn',
        'Hiển', 'Thị', 'Tạo', 'Thêm', 'Chọn', 'Mở', 'Xóa', 'Cắt', 'Chạy', 'Xem', 'Kéo', 'Nhấn', 'Bấm', 'Ấn', 'Nói', 'Gõ', 'Cài', 'Tải', 'Chỉnh', 'Sửa', 'Xuất', 'Lưu', 'Đổi', 'Nhập',
        'Bành', 'Bôi', 'Băm', 'Bạn', 'Bất', 'Bắc', 'Bắt', 'Bằng', 'Bội', 'Cao', 'Chan', 'Chen', 'Chu', 'Chun', 'Chính', 'Chưa', 'Chỉ', 'Chị', 'Chồng', 'Chủ', 'Cách', 'Công', 'Cùng', 'Cảnh', 'Cấp', 'Cận', 'Duy', 'Dò', 'Dòng', 'Dùng', 'Dễ', 'Định', 'Đồng', 'Động', 'Đi', 'Điểm', 'Đều', 'Đưa', 'Đứng', 'Hình', 'Hành', 'Học', 'Hỏi', 'Hủy', 'Khu', 'Kho', 'Không', 'Khác', 'Khóa', 'Làm', 'Lên', 'Lại', 'Lấy', 'Lớp', 'Lần', 'Lớn', 'Mới', 'Một', 'Mọi', 'Nào', 'Này', 'Nhiều', 'Nhà', 'Nhìn', 'Nhớ', 'Phải', 'Phần', 'Phát', 'Phòng', 'Qua', 'Quản', 'Quá', 'Rồi', 'Sau', 'Sang', 'Số', 'Sắp', 'Thế', 'Thường', 'Thành', 'Thời gian', 'Thử', 'Tên', 'Tự', 'Tốc độ', 'Tới', 'Từng', 'Vào', 'Với', 'Việc', 'Xoá', 'Xử lý', 'Yêu cầu'
    }
    
    words = text.split()
    fixed_words = []
    for i, w in enumerate(words):
        match = re.match(r'^([^\w]*)([\w\d]+)([^\w]*)$', w, re.UNICODE)
        if match:
            prefix, core, suffix = match.groups()
            if core in proper_nouns:
                fixed_words.append(w)
            elif core in capcut_bad_caps or (core.isupper() and core not in proper_nouns and len(core) > 1):
                fixed_words.append(prefix + core.lower() + suffix)
            else:
                fixed_words.append(w)
        else:
            fixed_words.append(w)
            
    cleaned = ' '.join(fixed_words)

    # Viết hoa chữ cái đầu tiên
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]

    # Ngắt 2 dòng thông minh (Smart Balanced 2-Line Break)
    cleaned = smart_semantic_line_break(cleaned)

    return cleaned

def smart_semantic_line_break(text, max_single_line_chars=20, max_line_chars=26):
    text = text.strip().replace('
', ' ')
    text = re.sub(r'\s+', ' ', text)
    words = text.split()
    
    if len(words) <= 4 and len(text) <= max_single_line_chars:
        return text

    best_idx = None
    best_score = float('inf')
    
    major_connectors = {'mà', 'nhưng', 'để', 'thì', 'hoặc', 'vì', 'nếu', 'khi', 'bởi vì', 'cho nên', 'sao cho', 'sẽ'}
    minor_connectors = {'và', 'là', 'với', 'cho', 'của', 'trong', 'vào', 'ra', 'từ', 'nên'}

    min_words = 2 if len(words) >= 4 else 1

    for i in range(min_words, len(words) - min_words + 1):
        line1 = ' '.join(words[:i])
        line2 = ' '.join(words[i:])
        
        len1 = len(line1)
        len2 = len(line2)
        
        penalty = 0
        if len1 > max_line_chars:
            penalty += (len1 - max_line_chars) * 25
        if len2 > max_line_chars:
            penalty += (len2 - max_line_chars) * 25
            
        if len(text) > 24:
            if len1 < 8:
                penalty += (8 - len1) * 20
            if len2 < 8:
                penalty += (8 - len2) * 20

        char_diff = abs(len1 - len2)
        
        word_after_cut = words[i].lower().strip('.,?!:;"'')
        word_before_cut = words[i-1].strip()
        
        bonus = 0
        if word_before_cut.endswith((',', ';', ':', '!', '?')):
            bonus += 40
            
        if word_after_cut in major_connectors:
            bonus += 30
        elif word_after_cut in minor_connectors:
            bonus += 15
            
        score = char_diff * 1.2 + penalty - bonus
        
        if score < best_score:
            best_score = score
            best_idx = i

    if best_idx is not None and 0 < best_idx < len(words):
        line1 = ' '.join(words[:best_idx])
        line2 = ' '.join(words[best_idx:])
        return f"{line1}\n{line2}"
    
    return text

def build_words_tokens(text):
    words_tokens = []
    lines = text.split('
')
    for line_idx, line in enumerate(lines):
        words = line.split(' ')
        for w in words:
            if w:
                words_tokens.append(w)
                words_tokens.append(' ')
        if words_tokens and words_tokens[-1] == ' ':
            words_tokens.pop()
        if line_idx < len(lines) - 1:
            words_tokens.append('
')
    return words_tokens

def process_project_file(file_path, level=2):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return False, 0

    modified = False
    sub_count = 0
    texts = data.get('materials', {}).get('texts', [])
    for item in texts:
        item['force_apply_line_max_width'] = False
        item['line_max_width'] = 1.0
        item['fixed_width'] = -1.0
        item['fixed_height'] = -1.0

        raw_content = item.get('content', '')
        if raw_content and 'text' in raw_content:
            try:
                content_obj = json.loads(raw_content)
                txt = content_obj.get('text', '')
                if txt:
                    new_txt = clean_vietnamese_subtitles(txt, level=level)
                    if new_txt != txt or content_obj.get('text') != new_txt:
                        content_obj['text'] = new_txt
                        if 'styles' in content_obj and len(content_obj['styles']) > 0:
                            for st in content_obj['styles']:
                                if 'range' in st:
                                    st['range'] = [0, len(new_txt)]
                        item['content'] = json.dumps(content_obj, ensure_ascii=False)
                        item['recognize_text'] = new_txt.replace('
', ' ')
                        
                        if 'words' in item and isinstance(item['words'], dict):
                            dur = item.get('words', {}).get('end_time', [])
                            dur_ms = dur[-1] if dur else 2000
                            tokens = build_words_tokens(new_txt)
                            num_tokens = len(tokens)
                            if num_tokens > 0:
                                step = dur_ms / num_tokens
                                item['words']['start_time'] = [int(i * step) for i in range(num_tokens)]
                                item['words']['end_time'] = [int((i + 1) * step) for i in range(num_tokens)]
                                item['words']['text'] = tokens
                        
                        modified = True
                        sub_count += 1
            except Exception:
                pass

    if modified or len(texts) > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True, sub_count
    return False, 0

def main():
    parser = argparse.ArgumentParser(description="Tự động sửa và lọc phụ đề CapCut PC")
    parser.add_argument("project", nargs="?", default="", help="Tên thư mục project CapCut (để trống để lấy mới nhất)")
    parser.add_argument("--level", type=int, default=2, choices=[1, 2, 3], help="Cấp độ lọc từ: 1=Clean Raw, 2=Punchy Short-form (mặc định), 3=Action-driven")
    args = parser.parse_args()

    if args.project.strip():
        project_name = args.project.strip()
        capcut_dir = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
        project_folder = os.path.join(capcut_dir, project_name)
    else:
        project_name, project_folder = get_latest_project()

    if not project_name or not project_folder or not os.path.exists(project_folder):
        print("RESULT_JSON:" + json.dumps({"status": "error", "message": "Không tìm thấy dự án CapCut nào!"}))
        return

    draft_file = os.path.join(project_folder, "draft_info.json")
    if os.path.exists(draft_file):
        bak_file = os.path.join(project_folder, f"draft_info.json.bak_auto_{int(time.time())}")
        shutil.copyfile(draft_file, bak_file)

    updated_files = 0
    total_scanned = 0
    total_subs_fixed = 0

    for root, dirs, files in os.walk(project_folder):
        for f in files:
            if f.endswith('.json') or f.endswith('.tmp'):
                total_scanned += 1
                is_mod, count = process_project_file(os.path.join(root, f), level=args.level)
                if is_mod:
                    updated_files += 1
                    total_subs_fixed += count

    res = {
        "status": "success",
        "project_name": project_name,
        "project_folder": project_folder,
        "level": args.level,
        "updated_files": updated_files,
        "total_scanned": total_scanned,
        "subs_fixed": total_subs_fixed
    }
    print("RESULT_JSON:" + json.dumps(res, ensure_ascii=False))

if __name__ == "__main__":
    main()
