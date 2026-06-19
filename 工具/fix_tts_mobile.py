#!/usr/bin/env python3
"""修复移动端 TTS 无声问题：cancel/speak 之间加延迟。"""
import os
import re

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {
    '404.html', 'index.html', 'about.html', 'contact.html', 'privacy.html',
    'family-preview.html', 'learning-path-preview.html', 'quiz-preview.html',
    'pronunciation-demo.html', 'pronunciation-test.html',
    'og-image-generator.html',
    'google7d301929e65a4f2c.html', 'baidu_verify_codeva-uvo9gEjPEy.html',
    'daily-airport.html',  # 已有完整修复，跳过
}

# 旧代码模式
OLD_CANCEL = "window.speechSynthesis.cancel()"
NEW_CANCEL = "if(window.speechSynthesis.speaking)window.speechSynthesis.cancel()"

# speak(u) 需要用 setTimeout 包起来
# 找到 pattern: window.speechSynthesis.speak(u);
# 替换为: setTimeout(function(){window.speechSynthesis.speak(u);},20);

results = []
for fname in sorted(os.listdir(SITE_DIR)):
    if not fname.endswith('.html') or fname in SKIP:
        continue

    fpath = os.path.join(SITE_DIR, fname)
    html = open(fpath, encoding='utf-8').read()

    # 检查是否有TTS代码
    if 'speechSynthesis.speak' not in html:
        continue

    modified = False
    new_html = html

    # 修复1: 条件cancel
    if OLD_CANCEL in new_html:
        new_html = new_html.replace(OLD_CANCEL, NEW_CANCEL)
        modified = True

    # 修复2: speak(u) 加 setTimeout
    if 'window.speechSynthesis.speak(u);' in new_html:
        new_html = new_html.replace(
            'window.speechSynthesis.speak(u);',
            'setTimeout(function(){window.speechSynthesis.speak(u);},20);'
        )
        modified = True

    if modified:
        open(fpath, 'w', encoding='utf-8').write(new_html)
        results.append(('FIX', fname))
    else:
        results.append(('OK', fname))

print(f"修复: {sum(1 for a,_ in results if a=='FIX')}  未改: {sum(1 for a,_ in results if a=='OK')}")
for a, f in results:
    print(f"  {a:>4}  {f}")
