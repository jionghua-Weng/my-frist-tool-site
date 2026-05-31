#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Update audio injection script — add text highlight during playback."""

import sys, os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

OLD_MARKER = ".audio-btn.playing{background:#e74c3c"
NEW_CSS_INSERT = ".audio-highlight{background:#fff3b0;border-radius:4px;transition:background .3s}[data-theme=\"dark\"] .audio-highlight{background:#3d3520}"

OLD_SPEAK = "var voices=[];"
NEW_SPEAK = "var voices=[],curHL=null;"

OLD_SPEAK_START = "function speak(t,b){"
NEW_SPEAK_START = """function speak(t,b,el){
if(curHL){curHL.classList.remove('audio-highlight');curHL=null}"""

OLD_SPEAK_CANCEL = "window.speechSynthesis.cancel();"
NEW_SPEAK_CANCEL = "window.speechSynthesis.cancel();"

OLD_BTN_PLAYING = "b.classList.add('playing');"
NEW_BTN_PLAYING = "b.classList.add('playing');\nif(el){el.classList.add('audio-highlight');curHL=el}"

OLD_ONEND = "u.onend=u.onerror=function(){b.classList.remove('playing')};"
NEW_ONEND = "u.onend=u.onerror=function(){b.classList.remove('playing');if(el){el.classList.remove('audio-highlight');curHL=null}};"

OLD_MKBTN_CLICK = "speak(txt,btn)"
NEW_MKBTN_CLICK = "speak(txt,btn,el)"


def update_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if NEW_CSS_INSERT in content:
        return False, "已更新，跳过"

    if OLD_MARKER not in content:
        return False, "找不到音频脚本"

    # 1. Add highlight CSS after the dark mode playing rule
    old_css_end = "[data-theme=\"dark\"] .audio-btn.playing{background:#ef4444}'"
    new_css_end = "[data-theme=\"dark\"] .audio-btn.playing{background:#ef4444}" + NEW_CSS_INSERT + "'"
    content = content.replace(old_css_end, new_css_end, 1)

    # 2. Add curHL variable
    content = content.replace(OLD_SPEAK, NEW_SPEAK, 1)

    # 3. Update speak() function signature and body
    content = content.replace(OLD_SPEAK_START, NEW_SPEAK_START, 1)
    content = content.replace(OLD_BTN_PLAYING, NEW_BTN_PLAYING, 1)
    content = content.replace(OLD_ONEND, NEW_ONEND, 1)

    # 4. Update mkBtn call to pass el
    content = content.replace(OLD_MKBTN_CLICK, NEW_MKBTN_CLICK, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True, "OK"


def main():
    files = sys.argv[1:]
    if not files:
        print("Usage: python update_audio_highlight.py <files...>")
        sys.exit(1)

    ok = 0
    for f in sorted(files):
        if not os.path.isfile(f):
            print(f"  [MISS] {f}")
            continue
        success, reason = update_file(f)
        tag = "[OK]" if success else "[SKIP]"
        print(f"  {tag} {os.path.basename(f):45s} {reason}")
        if success:
            ok += 1
    print(f"\nDone: {ok}/{len(files)}")


if __name__ == "__main__":
    main()
