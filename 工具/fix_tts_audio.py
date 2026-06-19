#!/usr/bin/env python3
"""用 HTML5 Audio + 百度 TTS 替换 Web Speech API。"""
import os

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {
    '404.html','index.html','about.html','contact.html','privacy.html',
    'family-preview.html','learning-path-preview.html','quiz-preview.html',
    'pronunciation-demo.html','pronunciation-test.html','og-image-generator.html',
    'google7d301929e65a4f2c.html','baidu_verify_codeva-uvo9gEjPEy.html',
    'daily-airport.html',
}

def extract_speak_func(lines, start_idx):
    """提取 speak 函数：从 start_idx 找到匹配的 }"""
    depth = 0
    started = False
    end_idx = start_idx
    for i in range(start_idx, len(lines)):
        line = lines[i]
        for ch in line:
            if ch == '{':
                depth += 1
                started = True
            elif ch == '}':
                depth -= 1
                if started and depth == 0:
                    end_idx = i
                    return end_idx
    return start_idx + 10  # fallback

results = []
for fname in sorted(os.listdir(SITE_DIR)):
    if not fname.endswith('.html') or fname in SKIP: continue
    fpath = os.path.join(SITE_DIR, fname)
    lines = open(fpath, encoding='utf-8').readlines()

    if not any('speechSynthesis' in l for l in lines):
        continue
    if any('fanyi.baidu.com/gettts' in l for l in lines):
        continue

    # 找 speak 函数起始行
    speak_start = None
    for i, line in enumerate(lines):
        if 'function speak(t,b,el){' in line:
            speak_start = i
            break
    if speak_start is None:
        results.append(('NOSTART', fname))
        continue

    speak_end = extract_speak_func(lines, speak_start)

    # 新函数（纯 Audio，不用 Web Speech API）
    indent = ' ' * (len(lines[speak_start]) - len(lines[speak_start].lstrip()))
    new_func = f"""{indent}function speak(t,b,el){{
{indent}if(curHL){{curHL.classList.remove('audio-highlight');curHL=null}}
{indent}t=t.replace(/\\s?\\/[^\\/]*[^\\x00-\\x7F][^\\/]*\\/\\s?/g,' ').replace(/\\s+/g,' ').trim();
{indent}b.classList.add('playing');
{indent}if(el){{el.classList.add('audio-highlight');curHL=el}}
{indent}var a=new Audio();
{indent}a.src='https://fanyi.baidu.com/gettts?lan=en&text='+encodeURIComponent(t)+'&spd=3';
{indent}a.onended=a.onerror=function(){{b.classList.remove('playing');if(el){{el.classList.remove('audio-highlight');curHL=null}}}};
{indent}a.play();
{indent}}}"""
    new_lines = lines[:speak_start] + [new_func + '\n'] + lines[speak_end+1:]

    # 清理残留的 speechSynthesis 和 voice 相关代码
    clean = []
    for line in new_lines:
        # 跳过 speechSynthesis 初始化行
        if 'var ttsOk=' in line and 'speechSynthesis' in line:
            clean.append(line.replace(
                'var ttsOk=!!window.speechSynthesis,voices=[],curHL=null;',
                'var curHL=null;'
            ))
            continue
        if 'if(ttsOk){function lv()' in line:
            continue
        if 'function gv(){' in line and 'voices.find' in line:
            continue
        clean.append(line)

    open(fpath, 'w', encoding='utf-8').writelines(clean)
    results.append(('FIX', fname))

print(f"修复: {len(results)}")
for r in results:
    if r[0] != 'FIX': print(f"  {r[0]:>7}  {r[1]}")
