"""
修复安卓手机端看不到点读按钮的问题。
根因: if(!window.speechSynthesis)return; 在按钮创建之前就退出了。
方案:
  1. 移除脚本顶部的 early return
  2. 在 speak() 函数内部加 guard，不支持的浏览器点按钮无反应
  3. 按钮始终创建，CSS 始终注入
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

    # 修复1: 移除顶部 early return
    old1 = "if(!window.speechSynthesis)return;\nvar voices=[]"
    new1 = "var voices=[]"
    if old1 in content:
        content = content.replace(old1, new1)
        modified = True

    # 修复2: 在 speak() 函数体开头加 guard
    old2 = "function speak(t,b,el){\nt=t.replace"
    new2 = "function speak(t,b,el){\nif(!window.speechSynthesis)return;\nt=t.replace"
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
