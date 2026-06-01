"""
.article 容器加 overflow-wrap:break-word + overflow-x:hidden
防止任何内容在QQ浏览器窄屏溢出。
"""
import os, sys, io, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    old = ".article{max-width:800px;margin:60px auto;padding:0 20px}"
    if old not in content:
        return False

    new = ".article{max-width:800px;margin:60px auto;padding:0 20px;overflow-wrap:break-word}"
    content = content.replace(old, new)
    modified = True

    # Also fix .page-content pages (about, contact, privacy)
    old2 = ".page-content{max-width:800px;margin:60px auto;padding:0 20px}"
    if old2 in content:
        new2 = ".page-content{max-width:800px;margin:60px auto;padding:0 20px;overflow-wrap:break-word}"
        content = content.replace(old2, new2)
        modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return modified

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
