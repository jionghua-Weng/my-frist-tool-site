"""
修复安卓 TTS 初始化崩溃导致按钮不显示。
问题: lv() 调用 speechSynthesis.getVoices() 在 undefined 上崩溃。
修复: ttsOk 变量控制，TTS 不可用时跳过初始化，按钮正常渲染。
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

    # 修复1: TTS 初始化包在 if(ttsOk) 里
    old1 = "document.head.appendChild(s);\nvar voices=[],curHL=null;\nfunction lv(){voices=window.speechSynthesis.getVoices()}\nlv();window.speechSynthesis.onvoiceschanged=lv;"
    new1 = "document.head.appendChild(s);\nvar ttsOk=!!window.speechSynthesis,voices=[],curHL=null;\nif(ttsOk){function lv(){voices=window.speechSynthesis.getVoices()}lv();window.speechSynthesis.onvoiceschanged=lv}"
    if old1 in content:
        content = content.replace(old1, new1)
        modified = True

    # 修复2: speak() 内用 ttsOk 变量替代 window.speechSynthesis 判断
    old2 = "if(!window.speechSynthesis)return;"
    new2 = "if(!ttsOk)return;"
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
