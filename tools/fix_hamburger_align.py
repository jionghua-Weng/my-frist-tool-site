"""
修复移动端头部三条横(汉堡菜单)与小太阳、放大镜不在同一水平线。
根因: min-height:44px 撑高汉堡按钮, 但内部3条线贴顶部,
      而 theme-toggle/srch-btn 的 SVG 是居中的。
修复: hamburger 加 justify-content:center
"""
import os, sys, io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 两种CSS格式: minified 和 expanded
FIXES = [
    # minified CSS
    {
        "old": ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px;min-width:44px;min-height:44px}",
        "new": ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px;min-width:44px;min-height:44px;justify-content:center}",
    },
    # expanded CSS variant 1
    {
        "old": "    padding: 8px;\n    flex-direction: column;\n    gap: 5px;\n    min-width: 44px;\n    min-height: 44px;",
        "new": "    padding: 8px;\n    flex-direction: column;\n    gap: 5px;\n    min-width: 44px;\n    min-height: 44px;\n    justify-content: center;",
    },
]

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    for fix in FIXES:
        if fix["old"] in content and fix["new"] not in content:
            content = content.replace(fix["old"], fix["new"])
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
