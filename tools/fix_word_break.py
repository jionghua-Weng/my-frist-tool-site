"""
vocab-table 加 word-break:break-word, 防止长单词在窄屏撑开页面。
"""
import os, sys, io, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # vocab-table td (minified)
    old_td = ".vocab-table td{border-bottom:1px solid #e5e7eb;padding:12px 16px;font-size:16px}"
    new_td = ".vocab-table td{border-bottom:1px solid #e5e7eb;padding:12px 16px;font-size:16px;word-break:break-word}"
    if old_td in content:
        content = content.replace(old_td, new_td)
        modified = True

    # vocab-table th (minified)
    old_th = ".vocab-table th{background:var(--navy);color:var(--white);padding:12px 16px;text-align:left;font-size:15px}"
    new_th = ".vocab-table th{background:var(--navy);color:var(--white);padding:12px 16px;text-align:left;font-size:15px;word-break:break-word}"
    if old_th in content:
        content = content.replace(old_th, new_th)
        modified = True

    # example .en — long English sentences
    old_en = ".article .example .en{font-size:20px;color:var(--text-dark);font-weight:600;margin-bottom:4px}"
    new_en = ".article .example .en{font-size:20px;color:var(--text-dark);font-weight:600;margin-bottom:4px;overflow-wrap:break-word}"
    if old_en in content:
        content = content.replace(old_en, new_en)
        modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    html_files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    fixed = 0
    for fname in html_files:
        filepath = os.path.join(ROOT, fname)
        if fix_file(filepath):
            fixed += 1
    print(f"修复: {fixed} 个文件")

if __name__ == "__main__":
    main()
