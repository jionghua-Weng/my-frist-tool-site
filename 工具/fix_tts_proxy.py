#!/usr/bin/env python3
"""替换 Web Speech API 为 HTML5 Audio + 自己的 TTS 代理。"""
import os

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {
    '404.html','index.html','about.html','contact.html','privacy.html',
    'family-preview.html','learning-path-preview.html','quiz-preview.html',
    'pronunciation-demo.html','pronunciation-test.html','og-image-generator.html',
    'google7d301929e65a4f2c.html','baidu_verify_codeva-uvo9gEjPEy.html',
    'tts-test.html',  # 测试页单独处理
}

def extract_brace_block(lines, start_idx):
    depth = 0; started = False
    for i in range(start_idx, len(lines)):
        for ch in lines[i]:
            if ch == '{': depth += 1; started = True
            elif ch == '}':
                depth -= 1
                if started and depth == 0: return i
    return start_idx + 10

results = []
for fname in sorted(os.listdir(SITE_DIR)):
    if not fname.endswith('.html') or fname in SKIP: continue
    fpath = os.path.join(SITE_DIR, fname)
    lines = open(fpath, encoding='utf-8').readlines()

    if not any('speechSynthesis' in l for l in lines): continue
    if '/tts.php' in ''.join(lines): continue

    # 找 speak 函数
    speak_start = None
    for i, line in enumerate(lines):
        if 'function speak(t,b,el){' in line:
            speak_start = i; break
    if speak_start is None: continue

    speak_end = extract_brace_block(lines, speak_start)
    indent = ' ' * (len(lines[speak_start]) - len(lines[speak_start].lstrip()))

    new_func = f"""{indent}function speak(t,b,el){{
{indent}if(curHL){{curHL.classList.remove('audio-highlight');curHL=null}}
{indent}t=t.replace(/\\s?\\/[^\\/]*[^\\x00-\\x7F][^\\/]*\\/\\s?/g,' ').replace(/\\s+/g,' ').trim();
{indent}b.classList.add('playing');
{indent}if(el){{el.classList.add('audio-highlight');curHL=el}}
{indent}var a=new Audio();
{indent}a.src='/tts.php?q='+encodeURIComponent(t);
{indent}a.onended=a.onerror=function(){{b.classList.remove('playing');if(el){{el.classList.remove('audio-highlight');curHL=null}}}};
{indent}a.play();
{indent}}}"""

    new_lines = lines[:speak_start] + [new_func + '\n'] + lines[speak_end+1:]

    # 清理
    clean = []
    for line in new_lines:
        if 'var ttsOk=' in line and 'speechSynthesis' in line:
            clean.append(line.replace(
                'var ttsOk=!!window.speechSynthesis,voices=[],curHL=null;',
                'var curHL=null;'))
            continue
        if 'if(ttsOk){function lv()' in line: continue
        if 'function gv(){' in line and 'voices.find' in line: continue
        clean.append(line)

    open(fpath, 'w', encoding='utf-8').writelines(clean)
    results.append(('FIX', fname))

# 同时更新测试页
test_path = os.path.join(SITE_DIR, 'tts-test.html')
if os.path.exists(test_path):
    test_html = open(test_path, encoding='utf-8').read()
    test_html = test_html.replace(
        "a.src='https://fanyi.baidu.com/gettts?lan=en&text='+encodeURIComponent(t)+'&spd=3';",
        "a.src='/tts.php?q='+encodeURIComponent(t);"
    )
    open(test_path, 'w', encoding='utf-8').write(test_html)
    results.append(('FIX', 'tts-test.html'))

print(f"修复: {len(results)}")
