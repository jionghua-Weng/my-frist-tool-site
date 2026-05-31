#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix: strip IPA phonetic notation from text before TTS speak()."""

import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Find old speak function body and add IPA cleaning
OLD_SPEAK = "function speak(t,b,el){"
NEW_SPEAK = """function speak(t,b,el){
t=t.replace(/\\s?\\/[^\\/]*[^\\x00-\\x7F][^\\/]*\\/\\s?/g,' ').replace(/\\s+/g,' ').trim();"""

OLD_MKBTN = "speak(txt,btn,el)"
# No change to mkBtn, but we add text cleaning in speak()

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'x00-\\x7F' in content or 'x00-\\\\x7F' in content:
        return False, "已修复，跳过"

    if 'if(curHL){curHL.classList.remove' not in content:
        return False, "无音频脚本"

    # Replace the speak function
    if OLD_SPEAK not in content:
        return False, "speak函数不匹配"

    content = content.replace(OLD_SPEAK, NEW_SPEAK, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True, "OK"


def main():
    files = sys.argv[1:]
    if not files:
        print("Usage: python fix_ipa_strip.py <files...>")
        sys.exit(1)

    ok = 0
    for f in sorted(files):
        if not os.path.isfile(f):
            continue
        success, reason = fix_file(f)
        tag = "[OK]" if success else "[SKIP]"
        print(f"  {tag} {os.path.basename(f):45s} {reason}")
        if success:
            ok += 1
    print(f"\nDone: {ok}/{len(files)}")


if __name__ == "__main__":
    main()
