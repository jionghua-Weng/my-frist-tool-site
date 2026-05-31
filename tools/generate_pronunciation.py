#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate pronunciation clinic preview pages."""

import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'daily-coffee.html')
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

def load_tpl():
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        return f.read()

def write_article(filename, title_tag, desc, h1, breadcrumb, url, html):
    tpl = load_tpl()
    out = tpl
    # Replace all the template-specific strings
    out = out.replace('用英文点咖啡：不只是"Coffee, please" — 场景口语 | 英语研习社', title_tag)
    out = out.replace('从星巴克到精品咖啡馆，一篇搞懂用英文点咖啡的全部用语。卡布奇诺、拿铁、半糖、去冰——所有你需要的表达都在这里。', desc)
    out = out.replace('用英文点咖啡：不只是&quot;Coffee, please&quot; — 场景口语 | 英语研习社', title_tag.replace('"', '&quot;'))
    out = out.replace('content="https://easyeng.club/daily-coffee.html"', f'content="https://easyeng.club/{filename}"')
    # Replace h1
    old_h1 = '<h1>用英文点咖啡：不只是"Coffee, please"</h1>'
    out = out.replace(old_h1, f'<h1>{h1}</h1>', 1)
    # Replace breadcrumb
    old_bread = '<div class="breadcrumb"><a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 用英文点咖啡：不只是"Coffee, please"</div>'
    out = out.replace(old_bread, f'<div class="breadcrumb">{breadcrumb}</div>', 1)

    # Replace article content
    meta_end = out.find('</div>', out.find('class="meta"')) + 6
    rel_start = out.find('<div class="related">')

    prefix = out[:meta_end]
    suffix = out[out.find('</main>'):]

    new_content = prefix + '\n' + html + '\n</main>' + suffix
    filepath = os.path.join(OUTDIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'  [OK] {filename}')

# ======= Article 1: th sound =======
th_html = '''<p>英语里有两个音，中文完全没有——<strong>/θ/ 和 /ð/</strong>，也就是俗称的"咬舌音"。发这两个音时，舌尖要轻轻伸到上下牙齿之间。很多中国学习者用 /s/ 或 /z/ 来代替，结果 think 说成了 sink，thank 说成了 sank。这篇帮你一次性纠正。</p>

<h2>两个 th 音怎么发？</h2>

<p><strong>/θ/ — 清辅音</strong>：舌尖伸到齿间，气流从舌齿缝隙挤出，声带不振动。类似用舌头堵住"嘶"声。</p>
<div class="example"><div class="en">think /θɪŋk/</div><div class="zh">想</div></div>
<div class="example"><div class="en">three /θriː/</div><div class="zh">三</div></div>
<div class="example"><div class="en">thank /θæŋk/</div><div class="zh">谢谢</div></div>
<div class="example"><div class="en">mouth /maʊθ/</div><div class="zh">嘴巴（注意词尾也要咬舌）</div></div>

<p><strong>/ð/ — 浊辅音</strong>：舌尖位置同上，但声带振动。类似用舌头堵住"滋"声，同时喉咙发声。</p>
<div class="example"><div class="en">this /ðɪs/</div><div class="zh">这个</div></div>
<div class="example"><div class="en">that /ðæt/</div><div class="zh">那个</div></div>
<div class="example"><div class="en">the /ðə/</div><div class="zh">这个/那个（最常用的词，一定要发对）</div></div>
<div class="example"><div class="en">breathe /briːð/</div><div class="zh">呼吸（动词，词尾发 /ð/）</div></div>

<h2>对比练习：你嘴里发出的到底是哪个？</h2>

<p>每对词只差一个音，意思却完全不同。点喇叭分别听，体会差别：</p>

<h3>第1组：th /θ/ vs s /s/</h3>
<div class="example"><div class="en">think /θɪŋk/ — 想</div><div class="zh">正确：舌尖伸出来，气流通过齿间。</div></div>
<div class="example"><div class="en">sink /sɪŋk/ — 下沉</div><div class="zh">错误：舌尖在牙齿后面，上下牙咬合。think ≠ sink！</div></div>

<div class="example"><div class="en">thick /θɪk/ — 厚的</div><div class="zh">咬舌。</div></div>
<div class="example"><div class="en">sick /sɪk/ — 生病的</div><div class="zh">不咬舌。thick ≠ sick！</div></div>

<h3>第2组：th /θ/ vs t /t/（很多人用 t 代替 th）</h3>
<div class="example"><div class="en">three /θriː/ — 三</div><div class="zh">正确：先咬舌，再收舌发 r。</div></div>
<div class="example"><div class="en">tree /triː/ — 树</div><div class="zh">错误：舌尖顶住上颚。three ≠ tree！</div></div>

<h3>第3组：th /ð/ vs d /d/（"this"说成"dis"）</h3>
<div class="example"><div class="en">this /ðɪs/ — 这个</div><div class="zh">舌尖伸出来一点，声带振动。</div></div>
<div class="example"><div class="en">dis /dɪs/ — （俚语：不尊重）</div><div class="zh">舌尖顶住上颚弹出。this ≠ dis！</div></div>

<div class="example"><div class="en">they /ðeɪ/ — 他们</div><div class="zh">咬舌出声。</div></div>
<div class="example"><div class="en">day /deɪ/ — 日子</div><div class="zh">不咬舌。they ≠ day！</div></div>

<h2>实战：含 th 的常用句子</h2>
<p>每句都包含至少一个 th 音，练到脱口而出：</p>

<div class="example"><div class="en">Thank you for thinking of me. That's very thoughtful.</div><div class="zh">谢谢你想到我，太贴心了。（3个 th 音：thank, thinking, thoughtful）</div></div>

<div class="example"><div class="en">The weather this Thursday might be better than this.</div><div class="zh">这周四天气可能比今天好。（4个 th 音：the, this, Thursday, this）</div></div>

<div class="example"><div class="en">I think there are three things I need to tell you.</div><div class="zh">我觉得有三件事要告诉你。（3个 th 音：think, three, things）</div></div>

<div class="example"><div class="en">Neither my father nor my mother likes this weather either.</div><div class="zh">我爸我妈都不喜欢这天气。（3个 th 音：father, mother, weather）</div></div>

<h2>小技巧：怎么判断该发哪个 th？</h2>
<table class="vocab-table">
<tr><th>规律</th><th>/θ/ 清辅音</th><th>/ð/ 浊辅音</th></tr>
<tr><td>词首</td><td>实义词：think, three, thank, thick, thumb</td><td>功能词：the, this, that, these, those, they, there</td></tr>
<tr><td>词中</td><td>通常 /θ/：nothing, author, method</td><td>通常 /ð/：mother, father, weather, either</td></tr>
<tr><td>词尾</td><td>名词/形容词：mouth, teeth, tooth, north</td><td>动词：breathe, bathe, clothe</td></tr>
</table>
<p>最简单的口诀：<strong>功能词（the/this/that/they）基本都用 /ð/，实义词（think/three/thick）基本都用 /θ/</strong>。</p>'''

write_article(
    'pronunciation-th-sound.html',
    '"Think" or "Sink"? — 搞定英语最难发的 th 音 | 发音诊所 | 英语研习社',
    '英语th音发音完全指南：/θ/和/ð/的区别，think vs sink对比练习，中文母语者专属纠音教程。含音频点读对比。',
    '"Think" or "Sink"? — 搞定英语最难发的 th 音',
    '<a href="index.html">首页</a> &raquo; <a href="pronunciation.html">发音诊所</a> &raquo; th 音：think vs sink',
    'pronunciation-th-sound.html',
    th_html
)

print('\\nPreview files created. Now creating list page...')
