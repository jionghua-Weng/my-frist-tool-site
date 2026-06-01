"""
统一三个头部按钮的高度和对齐方式:
- 全部: height:44px;width:44px;padding:0;display:flex
- hamburger: flex-direction:column;gap:6px;justify-content:center
- theme-toggle/srch-btn: align-items:center;justify-content:center
"""
import os, sys, io, re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False
    # Track which format we're dealing with
    is_minified = '.hamburger{' in content and '\n' not in content.split('.hamburger{')[1].split('}')[0] if '.hamburger{' in content else False

    # --- Fix 1: hamburger ---
    # Target: display:none;background:none;border:none;cursor:pointer;padding:0;flex-direction:column;gap:6px;min-width:44px;height:44px;justify-content:center;align-items:center

    # Minified old patterns (various versions from previous fixes)
    old_hamburgers_min = [
        ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px;min-width:44px;min-height:44px;justify-content:center}",
        ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px;min-width:44px;min-height:44px}",
        ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:8px;flex-direction:column;gap:5px}",
    ]
    new_hamburger_min = ".hamburger{display:none;background:none;border:none;cursor:pointer;padding:0;flex-direction:column;gap:6px;min-width:44px;height:44px;justify-content:center;align-items:center}"

    for old in old_hamburgers_min:
        if old in content:
            content = content.replace(old, new_hamburger_min)
            modified = True
            break

    # Expanded old pattern
    old_hamburger_exp = "    padding: 8px;\n    flex-direction: column;\n    gap: 5px;"
    new_hamburger_exp = "    padding: 0;\n    flex-direction: column;\n    gap: 6px;\n    min-width: 44px;\n    height: 44px;\n    justify-content: center;\n    align-items: center;"
    if old_hamburger_exp in content:
        content = content.replace(old_hamburger_exp, new_hamburger_exp)
        modified = True

    # --- Fix 2: theme-toggle ---
    old_themes_min = [
        ".theme-toggle{background:none;border:none;cursor:pointer;padding:6px 8px;color:var(--white);display:flex;align-items:center;flex-shrink:0;min-width:44px;min-height:44px}",
    ]
    new_theme_min = ".theme-toggle{background:none;border:none;cursor:pointer;padding:0;color:var(--white);display:flex;align-items:center;justify-content:center;flex-shrink:0;min-width:44px;height:44px}"

    for old in old_themes_min:
        if old in content:
            content = content.replace(old, new_theme_min)
            modified = True
            break

    # --- Fix 3: srch-btn ---
    old_search_min = [
        ".srch-btn{background:none;border:none;cursor:pointer;padding:6px 8px;margin-left:4px;color:#fff;display:flex;align-items:center;border-radius:6px;transition:background .2s;min-width:44px;min-height:44px}",
    ]
    new_search_min = ".srch-btn{background:none;border:none;cursor:pointer;padding:0;margin-left:4px;color:#fff;display:flex;align-items:center;justify-content:center;border-radius:6px;transition:background .2s;min-width:44px;height:44px}"

    for old in old_search_min:
        if old in content:
            content = content.replace(old, new_search_min)
            modified = True
            break

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
