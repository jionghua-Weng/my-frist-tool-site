"""
给所有裸 <table> 标签加上 class='vocab-table'。
无样式表格在 QQ 浏览器 X5 内核下渲染异常，导致页面错乱。
"""
import os, sys, io, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 只在 <main> 内替换裸 <table> 为 <table class="vocab-table">
    main_m = re.search(r'(<main[^>]*>.*?</main>)', content, re.DOTALL)
    if not main_m:
        return False

    main_content = main_m.group(1)
    old_main = main_content

    # 替换 <table> 或 <table > 为 <table class="vocab-table">
    # 但不替换已经有 class 的
    new_main = re.sub(
        r'<table\s*>',
        r'<table class="vocab-table">',
        main_content
    )

    if new_main == old_main:
        return False

    content = content.replace(old_main, new_main)
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

if __name__ == "__main__":
    main()
