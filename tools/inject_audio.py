#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Batch inject audio point-read script into HTML files before </body>"""

import sys, os, glob

# Fix Windows GBK encoding issue
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

INJECT = """<script>
(function(){
var s=document.createElement('style');
s.textContent='.audio-btn{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;margin-left:8px;background:var(--accent);color:#fff;border:none;border-radius:50%;cursor:pointer;font-size:14px;flex-shrink:0;vertical-align:middle;transition:background .2s,transform .15s}.audio-btn:hover{background:var(--accent-hover);transform:scale(1.1)}.audio-btn.playing{background:#e74c3c;animation:audioPulse .8s infinite}@keyframes audioPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}[data-theme="dark"] .audio-btn.playing{background:#ef4444}';
document.head.appendChild(s);
if(!window.speechSynthesis)return;
var voices=[];
function lv(){voices=window.speechSynthesis.getVoices()}
lv();window.speechSynthesis.onvoiceschanged=lv;
function gv(){var v=voices.find(function(x){return x.lang==='en-US'&&x.name.indexOf('Female')>=0});return v||voices.find(function(x){return x.lang.startsWith('en-')})||null}
function speak(t,b){
window.speechSynthesis.cancel();
var u=new SpeechSynthesisUtterance(t);
u.lang='en-US';u.rate=0.9;
var v=gv();if(v)u.voice=v;
b.classList.add('playing');
u.onend=u.onerror=function(){b.classList.remove('playing')};
window.speechSynthesis.speak(u);
}
var S='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 010 14.14"/><path d="M15.54 8.46a5 5 0 010 7.07"/></svg>';
function mkBtn(txt,el){
var btn=document.createElement('button');
btn.className='audio-btn';
btn.innerHTML=S;
btn.title='点击听发音';
btn.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();speak(txt,btn)});
el.appendChild(btn);
}
document.querySelectorAll('.example .en').forEach(function(el){mkBtn(el.textContent.trim(),el)});
document.querySelectorAll('.dialogue .line').forEach(function(el){
var c=el.cloneNode(true);var sp=c.querySelector('.speaker');if(sp)sp.remove();
var t=c.textContent.trim();if(t&&/[a-zA-Z]/.test(t)){mkBtn(t,el)}
});
})();
</script>
"""


def inject_file(filepath):
    """在文件 </body> 前注入脚本，返回 (ok, reason)"""
    if not os.path.isfile(filepath):
        return False, "文件不存在"

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 已经注入过？跳过
    if "audio-btn" in content:
        return False, "已注入，跳过"

    # 找到 </body>
    idx = content.rfind("</body>")
    if idx < 0:
        return False, "找不到 </body>"

    new_content = content[:idx] + INJECT + content[idx:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, "OK"


def main():
    if len(sys.argv) < 2:
        print("用法: python inject_audio.py <文件1> <文件2> ...")
        print("      或: python inject_audio.py <glob模式>")
        sys.exit(1)

    files = []
    for arg in sys.argv[1:]:
        matched = glob.glob(arg)
        if matched:
            files.extend(matched)
        else:
            files.append(arg)

    if not files:
        print("没有匹配到任何文件")
        sys.exit(1)

    print(f"Total: {len(files)} files\n")

    ok_count = 0
    for f in sorted(files):
        ok, reason = inject_file(f)
        tag = "[OK]" if ok else "[SKIP]"
        print(f"  {tag} {os.path.basename(f):45s} {reason}")
        if ok:
            ok_count += 1

    print(f"\nDone: {ok_count}/{len(files)}")


if __name__ == "__main__":
    main()
