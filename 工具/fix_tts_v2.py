#!/usr/bin/env python3
"""修复 TTS 移动端无声 v2：重写整个 speak 函数。"""
import os

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {
    '404.html','index.html','about.html','contact.html','privacy.html',
    'family-preview.html','learning-path-preview.html','quiz-preview.html',
    'pronunciation-demo.html','pronunciation-test.html','og-image-generator.html',
    'google7d301929e65a4f2c.html','baidu_verify_codeva-uvo9gEjPEy.html',
    'daily-airport.html',
}

NEW_FUNC_START = 'function speak(t,b,el){'
NEW_FUNC_BODY = r"""if(!ttsOk)return;
t=t.replace(/\s?\/[^\/]*[^\x00-\x7F][^\/]*\/\s?/g,' ').replace(/\s+/g,' ').trim();
if(curHL){curHL.classList.remove('audio-highlight');curHL=null}
var u=new SpeechSynthesisUtterance(t);
u.lang='en-US';u.rate=0.9;
var isMob=/Mobi|Android/i.test(navigator.userAgent);if(!isMob){var v=gv();if(v)u.voice=v;}
b.classList.add('playing');
if(el){el.classList.add('audio-highlight');curHL=el}
u.onend=u.onerror=function(){b.classList.remove('playing');if(el){el.classList.remove('audio-highlight');curHL=null}};
window.speechSynthesis.speak(u);
}"""

results = []
for fname in sorted(os.listdir(SITE_DIR)):
    if not fname.endswith('.html') or fname in SKIP: continue
    fpath = os.path.join(SITE_DIR, fname)
    html = open(fpath, encoding='utf-8').read()
    if 'function speak(t,b,el){' not in html: continue

    # 找 speak 函数起止位置
    start = html.index('function speak(t,b,el){')
    # 从函数体开始找匹配的 }
    depth = 0
    end = start
    in_func = False
    for i in range(start, len(html)):
        if html[i] == '{':
            depth += 1
            in_func = True
        elif html[i] == '}':
            depth -= 1
            if in_func and depth == 0:
                end = i + 1
                break

    new_html = html[:start] + NEW_FUNC_START + '\n' + NEW_FUNC_BODY + '\n' + html[end:]
    open(fpath, 'w', encoding='utf-8').write(new_html)
    results.append(('FIX', fname))

print(f"修复: {sum(1 for a in results if a[0]=='FIX')}")
for r in results:
    if r[0] != 'FIX': print(f"  {r[0]:>4}  {r[1]}  {r[2] if len(r)>2 else ''}")
