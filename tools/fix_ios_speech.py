"""
修复 iOS Safari SpeechSynthesis cancel+speak 竞态条件。
问题: cancel() 后立即 speak() 在 iOS 上静默失败, 音频不播放。
修复: speak 前加 20ms setTimeout, 让 iOS 处理完 cancel。
"""
import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 旧: cancel后立即speak (iOS会失败)
OLD = "window.speechSynthesis.speak(u);"
# 新: 20ms延迟
NEW = "setTimeout(function(){window.speechSynthesis.speak(u)},20);"

# 幂等检查: 已修复则跳过
ALREADY_FIXED = "setTimeout(function(){window.speechSynthesis.speak(u)}"

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if OLD not in content:
        return False
    if ALREADY_FIXED in content:
        return False  # 已修复, 跳过
    content = content.replace(OLD, NEW)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def main():
    html_files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    fixed = 0
    for fname in html_files:
        filepath = os.path.join(ROOT, fname)
        if fix_file(filepath):
            fixed += 1
    print(f"修复: {fixed} 个文件")
    print(f"跳过: {len(html_files) - fixed} 个文件")

if __name__ == "__main__":
    main()
