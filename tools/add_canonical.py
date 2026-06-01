"""
全站页面添加 canonical 标签，Google 识别规范 URL。
index.html → https://easyeng.club/
其他 → https://easyeng.club/filename.html
"""
import os, sys, io, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 非内容页，不添加 canonical
SKIP = {
    '404.html',
    'google7d301929e65a4f2c.html',
    'og-image-generator.html',
    'family-preview.html',
    'quiz-preview.html',
    'learning-path-preview.html',
    'pronunciation-demo.html',
    'pronunciation-test.html',
}

def fix_file(filepath, fname):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if '<link rel="canonical"' in content:
        return False  # 已存在

    if fname == 'index.html':
        canonical_url = 'https://easyeng.club/'
    else:
        canonical_url = f'https://easyeng.club/{fname}'

    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'

    # 插入到 viewport meta 之后
    if '<meta name="viewport"' in content:
        # 找到 viewport 那行的结尾 > 之后插入
        content = content.replace(
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n{canonical_tag}',
            1
        )
    elif '<meta charset="UTF-8">' in content:
        content = content.replace(
            '<meta charset="UTF-8">',
            f'<meta charset="UTF-8">\n{canonical_tag}',
            1
        )
    else:
        # 兜底：插入到 <title> 之前
        content = content.replace('<title>', f'{canonical_tag}\n<title>', 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return True

def main():
    html_files = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    fixed = 0
    skipped = 0
    for fname in html_files:
        if fname in SKIP:
            skipped += 1
            continue
        filepath = os.path.join(ROOT, fname)
        if fix_file(filepath, fname):
            fixed += 1
    print(f"添加: {fixed}, 跳过: {skipped}")

if __name__ == "__main__":
    main()
