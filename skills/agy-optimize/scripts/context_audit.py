import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import defaultdict

# --- Các hằng số cấu hình ---
RULE_BLOAT_THRESHOLD = 4 * 1024  # 4KB
TOTAL_RULE_BLOAT_THRESHOLD = 12 * 1024  # 12KB
SKILL_BLOAT_THRESHOLD = 20 * 1024  # 20KB
TOKEN_MULTIPLIER = 0.35

def detect_workflow_in_rule(content: str, file_size: int) -> bool:
    """Phát hiện xem rule có chứa workflow quá dài hay không."""
    if file_size <= RULE_BLOAT_THRESHOLD:
        return False
        
    # Đếm số lượng heading ### (dấu hiệu của sub-steps)
    h3_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
    
    # Đếm số code blocks
    code_blocks = len(re.findall(r'```', content)) / 2
    
    # Phát hiện numbered list > 5 items
    numbered_lists = re.finditer(r'(?:^\d+\.\s+.*(?:\n|$))+', content, re.MULTILINE)
    has_long_list = False
    for match in numbered_lists:
        lines = match.group(0).strip().split('\n')
        if len(lines) > 5:
            has_long_list = True
            break
            
    return (h3_count > 3) or (code_blocks > 0) or has_long_list

def extract_yaml_frontmatter(content: str) -> str:
    """Trích xuất frontmatter YAML từ nội dung markdown."""
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1)
    return ""

def get_yaml_description(frontmatter: str) -> str:
    """Trích xuất trường description từ frontmatter text."""
    for line in frontmatter.split('\n'):
        if line.startswith('description:'):
            return line.split('description:', 1)[1].strip().strip('\'"')
    return ""

def calculate_token_overlap(text1: str, text2: str) -> float:
    """Tính độ trùng lặp token (từ vựng) giữa 2 đoạn văn bản."""
    if not text1 or not text2:
        return 0.0
    tokens1 = set(re.findall(r'\w+', text1.lower()))
    tokens2 = set(re.findall(r'\w+', text2.lower()))
    
    if not tokens1 or not tokens2:
        return 0.0
        
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    
    return len(intersection) / len(union)

def get_dir_size(path: Path) -> int:
    """Đo tổng dung lượng của một thư mục."""
    total = 0
    try:
        for p in path.rglob('*'):
            if p.is_file():
                total += p.stat().st_size
    except Exception:
        pass
    return total

def audit(config_dir: str) -> Dict[str, Any]:
    """Hàm phân tích chính, quét các thư mục và trả về dictionary."""
    base_path = Path(config_dir).expanduser()
    
    results = {
        "config_dir": str(base_path),
        "rules": {"files": [], "total_size": 0, "bloated": 0, "workflow_in_rules": 0, "status": "OK"},
        "skills": {"total_count": 0, "total_size": 0, "bloated_skills": [], "similar_pairs": []},
        "mcp": {"servers": [], "error": None},
        "plugins": {"total_count": 0, "total_size": 0, "list": []},
        "workspace_rules": {"files": [], "total_size": 0},
        "health_score": 100,
        "estimated_tokens_per_turn": 0,
        "recommendations": []
    }
    
    total_context_bytes = 0  # Chỉ đếm bytes thực sự inject vào context
    total_skill_md_bytes = 0  # Riêng SKILL.md files
    
    # 1. Quét Rules (config/rules/)
    rules_dir = base_path / "rules"
    if rules_dir.exists() and rules_dir.is_dir():
        for file_path in rules_dir.glob("*.md"):
            try:
                size = file_path.stat().st_size
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.count('\n') + 1
                    
                is_bloated = size > RULE_BLOAT_THRESHOLD
                has_workflow = detect_workflow_in_rule(content, size)
                
                results["rules"]["files"].append({
                    "name": file_path.name,
                    "size": size,
                    "lines": lines,
                    "bloated": is_bloated,
                    "workflow_in_rule": has_workflow
                })
                
                results["rules"]["total_size"] += size
                total_context_bytes += size
                
                if is_bloated:
                    results["rules"]["bloated"] += 1
                    results["health_score"] -= 10
                    results["recommendations"].append({
                        "severity": "red",
                        "message": f"Rule {file_path.name} quá lớn ({size} bytes). Xem xét chia nhỏ."
                    })
                    
                if has_workflow:
                    results["rules"]["workflow_in_rules"] += 1
                    results["health_score"] -= 15
                    results["recommendations"].append({
                        "severity": "yellow",
                        "message": f"Rule {file_path.name} có dấu hiệu chứa workflow. Nên chuyển sang dạng Skill."
                    })
            except Exception as e:
                pass
                
        if results["rules"]["total_size"] > TOTAL_RULE_BLOAT_THRESHOLD:
            results["rules"]["status"] = "CONTEXT_BLOAT"
            results["health_score"] -= 20
            results["recommendations"].append({
                "severity": "red",
                "message": f"Tổng dung lượng rules quá lớn ({results['rules']['total_size']} bytes > 12KB)."
            })

    # 2. Quét Skills (config/skills/)
    skills_dir = base_path / "skills"
    if skills_dir.exists() and skills_dir.is_dir():
        results["skills"]["total_size"] = get_dir_size(skills_dir)
        # KHÔNG cộng total_size vào context — chỉ SKILL.md descriptions mới inject
        
        skills_info = []
        for skill_dir in [d for d in skills_dir.iterdir() if d.is_dir()]:
            results["skills"]["total_count"] += 1
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                try:
                    size = skill_md.stat().st_size
                    total_skill_md_bytes += size  # SKILL.md IS injected vào context
                    if size > SKILL_BLOAT_THRESHOLD:
                        results["skills"]["bloated_skills"].append(f"{skill_dir.name} ({size} bytes)")
                        results["health_score"] -= 5
                        results["recommendations"].append({
                            "severity": "yellow",
                            "message": f"Skill {skill_dir.name} quá lớn ({size} bytes)."
                        })
                        
                    with open(skill_md, 'r', encoding='utf-8') as f:
                        content = f.read()
                        frontmatter = extract_yaml_frontmatter(content)
                        desc = get_yaml_description(frontmatter)
                        skills_info.append({"name": skill_dir.name, "description": desc})
                except Exception:
                    pass
                    
        # Phát hiện mô tả skill trùng lặp
        for i in range(len(skills_info)):
            for j in range(i + 1, len(skills_info)):
                desc1 = skills_info[i]["description"]
                desc2 = skills_info[j]["description"]
                if desc1 and desc2:
                    overlap = calculate_token_overlap(desc1, desc2)
                    if overlap > 0.7:
                        results["skills"]["similar_pairs"].append((skills_info[i]["name"], skills_info[j]["name"]))
                        results["health_score"] -= 5
                        results["recommendations"].append({
                            "severity": "blue",
                            "message": f"Skills {skills_info[i]['name']} và {skills_info[j]['name']} có description giống nhau ({overlap*100:.1f}%)."
                        })

    # 3. Quét MCP Config (config/mcp_config.json)
    mcp_config = base_path / "mcp_config.json"
    if mcp_config.exists():
        try:
            with open(mcp_config, 'r', encoding='utf-8') as f:
                data = json.load(f)
                mcp_servers = data.get("mcpServers", {})
                for name, config in mcp_servers.items():
                    results["mcp"]["servers"].append({
                        "name": name,
                        "command": config.get("command", "")
                    })
        except Exception as e:
            results["mcp"]["error"] = str(e)
            
    # 4. Quét Plugins (config/plugins/)
    plugins_dir = base_path / "plugins"
    if plugins_dir.exists() and plugins_dir.is_dir():
        results["plugins"]["total_size"] = get_dir_size(plugins_dir)
        total_context_bytes += results["plugins"]["total_size"]
        for p in plugins_dir.iterdir():
            if p.is_dir() or p.is_file():
                results["plugins"]["total_count"] += 1
                results["plugins"]["list"].append(p.name)

    # 5. Quét Workspace Rules (hiện tại)
    current_dir = Path.cwd()
    workspace_md_files = list(current_dir.glob("*.md"))
    for file_path in workspace_md_files:
        try:
            size = file_path.stat().st_size
            results["workspace_rules"]["files"].append({
                "name": file_path.name,
                "size": size
            })
            results["workspace_rules"]["total_size"] += size
            total_context_bytes += size
            
            if size > RULE_BLOAT_THRESHOLD and file_path.name in ["AGENTS.md", "GEMINI.md"]:
                 results["recommendations"].append({
                    "severity": "yellow",
                    "message": f"Workspace rule {file_path.name} lớn ({size} bytes)."
                })
        except Exception:
            pass

    # 6. Chấm điểm tổng kết và ước tính token
    results["health_score"] = max(0, results["health_score"])
    # Context = rules + SKILL.md descriptions + workspace rules + plugins
    actual_context_bytes = (results["rules"]["total_size"] + 
                           total_skill_md_bytes + 
                           results["workspace_rules"]["total_size"] +
                           results["plugins"]["total_size"])
    results["estimated_tokens_per_turn"] = int(actual_context_bytes * TOKEN_MULTIPLIER)
    results["context_bytes_breakdown"] = {
        "rules": results["rules"]["total_size"],
        "skill_descriptions": total_skill_md_bytes,
        "workspace_rules": results["workspace_rules"]["total_size"],
        "plugins": results["plugins"]["total_size"],
        "total": actual_context_bytes
    }
    
    if results["health_score"] == 100:
        results["recommendations"].append({
            "severity": "green",
            "message": "Hệ thống khoẻ mạnh, context gọn gàng."
        })
        
    return results

def print_text_report(results: Dict[str, Any]):
    """In báo cáo định dạng Text cơ bản."""
    print("="*60)
    print("🧠 ANTIGRAVITY CONTEXT AUDIT REPORT")
    print("="*60)
    
    print(f"\n📂 Thư mục cấu hình: {results['config_dir']}")
    print(f"🏥 Health Score: {results['health_score']}/100")
    print(f"🪙 Estimated Tokens/Turn: ~{results['estimated_tokens_per_turn']} tokens")
    
    print("\n📜 RULES AUDIT:")
    print(f"  Trạng thái: {results['rules']['status']}")
    print(f"  Tổng dung lượng: {results['rules']['total_size']} bytes")
    for r in results['rules']['files']:
        bloat_str = "⚠️ BLOATED" if r['bloated'] else "✅ OK"
        wf_str = "🔄 WORKFLOW IN RULE" if r['workflow_in_rule'] else ""
        print(f"  - {r['name']}: {r['size']} bytes, {r['lines']} lines [{bloat_str}] {wf_str}")
        
    print("\n🛠️ SKILLS AUDIT:")
    print(f"  Tổng số skill: {results['skills']['total_count']}")
    print(f"  Tổng dung lượng: {results['skills']['total_size']} bytes")
    if results['skills']['bloated_skills']:
        print("  ⚠️ Bloated skills:", ", ".join(results['skills']['bloated_skills']))
    if results['skills']['similar_pairs']:
        print("  🔄 Trùng lặp description:")
        for p1, p2 in results['skills']['similar_pairs']:
            print(f"    - {p1} & {p2}")
            
    print("\n🔌 MCP SERVERS:")
    if results["mcp"]["error"]:
        print(f"  Lỗi đọc config: {results['mcp']['error']}")
    else:
        for s in results['mcp']['servers']:
            print(f"  - {s['name']} (cmd: {s['command']})")
            
    print("\n🧩 PLUGINS:")
    print(f"  Tổng số: {results['plugins']['total_count']} (Dung lượng: {results['plugins']['total_size']} bytes)")
    
    print("\n📁 WORKSPACE RULES:")
    print(f"  Tổng dung lượng: {results['workspace_rules']['total_size']} bytes")
    for f in results['workspace_rules']['files']:
        print(f"  - {f['name']}: {f['size']} bytes")
        
    print("\n💡 RECOMMENDATIONS:")
    for rec in results['recommendations']:
        sev_icon = {"green": "✅", "yellow": "⚠️", "red": "❌", "blue": "ℹ️"}.get(rec['severity'], "•")
        print(f"  {sev_icon} {rec['message']}")
    print("="*60)

def generate_markdown_report(results: Dict[str, Any], output_path: str):
    """Xuất báo cáo định dạng Markdown file."""
    lines = []
    lines.append("# 🧠 Antigravity Context Audit Report")
    lines.append("")
    lines.append(f"**Cấu hình:** `{results['config_dir']}`")
    lines.append(f"**Health Score:** `{results['health_score']}/100`")
    lines.append(f"**Ước tính Token/Turn:** `~{results['estimated_tokens_per_turn']} tokens`")
    lines.append("")
    
    lines.append("## 💡 Khuyến nghị")
    for rec in results['recommendations']:
        sev_icon = {"green": "✅", "yellow": "⚠️", "red": "❌", "blue": "ℹ️"}.get(rec['severity'], "•")
        lines.append(f"- {sev_icon} {rec['message']}")
    lines.append("")
    
    lines.append("## 📜 Rules")
    lines.append(f"- Trạng thái: **{results['rules']['status']}**")
    lines.append(f"- Tổng dung lượng: **{results['rules']['total_size']} bytes**")
    lines.append("")
    lines.append("| File | Size (bytes) | Lines | Status |")
    lines.append("|---|---|---|---|")
    for r in results['rules']['files']:
        status = []
        if r['bloated']: status.append("🔴 BLOATED")
        if r['workflow_in_rule']: status.append("🟠 WORKFLOW")
        if not status: status.append("🟢 OK")
        lines.append(f"| {r['name']} | {r['size']} | {r['lines']} | {', '.join(status)} |")
    lines.append("")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Đã xuất báo cáo ra {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Audit Antigravity Context Footprint")
    parser.add_argument("--config-dir", default="~/.gemini/config/", help="Thư mục cấu hình (mặc định: ~/.gemini/config/)")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả định dạng JSON")
    parser.add_argument("--report", action="store_true", help="Xuất báo cáo Markdown")
    
    args = parser.parse_args()
    
    results = audit(args.config_dir)
    
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.report:
        generate_markdown_report(results, "context_audit_report.md")
    else:
        print_text_report(results)

if __name__ == "__main__":
    main()
