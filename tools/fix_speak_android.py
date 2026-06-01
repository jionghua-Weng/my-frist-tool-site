"""
修复安卓点击不朗读。
问题: 无条件 cancel() + setTimeout 在 Android 上导致 speak 失败。
修复: 只在 speaking 时才 cancel, 去掉 setTimeout, 直接 speak()。
"""
import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 修复1: 条件cancel — 只在正在播放时才取消
    old1 = "window.speechSynthesis.cancel();"
    new1 = "if(window.speechSynthesis.speaking){window.speechSynthesis.cancel()}"
    if old1 in content:
        content = content.replace(old1, new1)
        modified = True

    # 修复2: 去掉 setTimeout, 直接 speak
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
