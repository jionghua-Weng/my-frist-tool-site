"""
回归最简单逻辑: 无条件 cancel + 直接 speak。
之前 iOS/Android 来回改引入了新问题，回到最初验证过的模式。
"""
import os, sys, io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 修复1: 改回无条件 cancel
    old1 = "if(window.speechSynthesis.speaking){window.speechSynthesis.cancel()}"
    new1 = "window.speechSynthesis.cancel()"
    if old1 in content:
        content = content.replace(old1, new1)
        modified = True

    # 修复2: 确保是直接 speak (不是 setTimeout)
    old2 = "setTimeout(function(){window.speechSynthesis.speak(u)},20);"
    new2 = "window.speechSynthesis.speak(u);"
    if old2 in content:
        content = content.replace(old2, new2)
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
