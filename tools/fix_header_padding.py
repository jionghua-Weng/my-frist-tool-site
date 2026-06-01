"""
header-inner 小屏收紧 padding：logo 和按钮组各自往左右靠。
- 959px 以下: padding 0 12px
- 640px 以下: padding 0 10px (更窄屏更紧)
"""
import os, sys, io, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # --- 959px 断点: 加 .header-inner{padding:0 12px} ---

    # Minified: @media(max-width:959px){...}
    old_959_min = "@media(max-width:959px){.main-nav{display:none}.hamburger{display:flex;margin-left:auto}.article h1{font-size:28px}.article h2{font-size:22px}}"
    new_959_min = "@media(max-width:959px){.header-inner{padding:0 12px}.main-nav{display:none}.hamburger{display:flex;margin-left:auto}.article h1{font-size:28px}.article h2{font-size:22px}}"
    if old_959_min in content:
        content = content.replace(old_959_min, new_959_min)
        modified = True

    # Minified variant (some pages have extra rules like .article table)
    # Use regex for minified 959px block
    def fix_959_minified(m):
        block = m.group(0)
        if '.header-inner{' in block:
            return block
        # Insert after the opening {
        return block.replace('{', '{.header-inner{padding:0 12px}', 1)

    pattern_959_min = r'@media\(max-width:959px\)\{[^}]+(?:\}[^}]+)*\}'
    # Simpler approach: just match the start pattern and replace
    old_959_start = "@media(max-width:959px){.main-nav{display:none}.hamburger{display:flex;margin-left:auto}"
    if old_959_start in content and '.header-inner{padding:0 12px}' not in content:
        content = content.replace(
            old_959_start,
            "@media(max-width:959px){.header-inner{padding:0 12px}.main-nav{display:none}.hamburger{display:flex;margin-left:auto}"
        )
        modified = True

    # Expanded: @media (max-width: 959px) { ... }
    old_959_exp = "@media (max-width: 959px) {"
    if old_959_exp in content and ".header-inner { padding: 0 12px;" not in content:
        content = content.replace(
            old_959_exp,
            "@media (max-width: 959px) {\n    .header-inner { padding: 0 12px; }"
        )
        modified = True

    # --- 640px 断点: 加/改 .header-inner padding ---

    # Minified: @media(max-width:640px){...}
    # Match the opening of 640px media query in minified CSS
    old_640_min = "@media(max-width:640px){.ad-slot:first-of-type{display:none}"
    if old_640_min in content and '.header-inner{padding:0 10px}' not in content:
        content = content.replace(
            old_640_min,
            "@media(max-width:640px){.header-inner{padding:0 10px}.ad-slot:first-of-type{display:none}"
        )
        modified = True

    # Minified variant without ad-slot
    old_640_min2 = "@media(max-width:640px){.article{margin:40px auto}"
    if old_640_min2 in content and '.header-inner{padding:0 10px}' not in content:
        content = content.replace(
            old_640_min2,
            "@media(max-width:640px){.header-inner{padding:0 10px}.article{margin:40px auto}"
        )
        modified = True

    # Expanded: @media (max-width: 640px) { ... }
    old_640_exp = "@media (max-width: 640px) {"
    if old_640_exp in content and ".header-inner { padding: 0 10px;" not in content:
        content = content.replace(
            old_640_exp,
            "@media (max-width: 640px) {\n    .header-inner { padding: 0 10px; }"
        )
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
        else:
            # Debug: show which files weren't modified
            pass
    print(f"修复: {fixed} 个文件")

if __name__ == "__main__":
    main()
