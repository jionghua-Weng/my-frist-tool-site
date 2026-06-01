"""
禁用 QQ浏览器/X5内核 字体自动增强。
全站 body 加 -webkit-text-size-adjust:100%;text-size-adjust:100%
"""
import os, sys, io, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 匹配 body CSS (minified): body{...-webkit-font-smoothing:antialiased}
    old_body_min = "-webkit-font-smoothing:antialiased}"
    new_body_min = "-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:100%;text-size-adjust:100%}"

    if old_body_min in content:
        content = content.replace(old_body_min, new_body_min)
        modified = True

    # 匹配 body CSS (expanded): -webkit-font-smoothing: antialiased;
    old_body_exp = "-webkit-font-smoothing: antialiased;\n}"
    new_body_exp = "-webkit-font-smoothing: antialiased;\n    -webkit-text-size-adjust: 100%;\n    text-size-adjust: 100%;\n}"

    if old_body_exp in content:
        content = content.replace(old_body_exp, new_body_exp)
        modified = True

    # 另一种 expanded 格式 (有些页面 body 后面紧接其他规则)
    old_body_exp2 = "-webkit-font-smoothing: antialiased;\n}\n"
    new_body_exp2 = "-webkit-font-smoothing: antialiased;\n    -webkit-text-size-adjust: 100%;\n    text-size-adjust: 100%;\n}\n"

    if old_body_exp2 in content and old_body_exp not in content:
        content = content.replace(old_body_exp2, new_body_exp2)
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
