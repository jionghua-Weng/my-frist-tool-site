#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate all 5 remaining pronunciation clinic articles."""

import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'daily-coffee.html')
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# Template strings to replace (from daily-coffee.html)
OLD_TITLE = '用英文点咖啡：不只是"Coffee, please" — 场景口语 | 英语研习社'
OLD_DESC = '从星巴克到精品咖啡馆，一篇搞懂用英文点咖啡的全部用语。卡布奇诺、拿铁、半糖、去冰——所有你需要的表达都在这里。'
OLD_OG_TITLE = '用英文点咖啡：不只是&quot;Coffee, please&quot; — 场景口语 | 英语研习社'
OLD_URL = 'content="https://easyeng.club/daily-coffee.html"'
OLD_H1 = '<h1>用英文点咖啡：不只是"Coffee, please"</h1>'
OLD_BREAD = '<div class="breadcrumb"><a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 用英文点咖啡：不只是"Coffee, please"</div>'

def load_tpl():
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        return f.read()

def write_article(filename, title_tag, desc, h1, breadcrumb, url, html, related=''):
    tpl = load_tpl()
    out = tpl
    out = out.replace(OLD_TITLE, title_tag)
    out = out.replace(OLD_DESC, desc)
    out = out.replace(OLD_OG_TITLE, title_tag.replace('"', '&quot;'))
    out = out.replace(OLD_URL, f'content="https://easyeng.club/{filename}"')
    out = out.replace(OLD_H1, f'<h1>{h1}</h1>', 1)
    out = out.replace(OLD_BREAD, f'<div class="breadcrumb">{breadcrumb}</div>', 1)

    # Replace article content
    meta_end = out.find('</div>', out.find('class="meta"')) + 6
    rel_start = out.find('<div class="related">')

    if related:
        related_html = f'<div class="related"><h3>相关文章</h3>{related}</div>'
    else:
        related_html = ''

    prefix = out[:meta_end]
    suffix = out[rel_start:] if rel_start > 0 else ''
    suffix = suffix[suffix.find('</main>'):] if '</main>' in suffix else '</main>\n' + out[out.find('<div class="ad-slot">'):]

    new_content = prefix + '\n' + html + '\n' + related_html + '\n</main>' + out[out.find('</main>')+7:] if '</main>' in out else ''

    # Simpler approach: just replace from meta_end to </main>
    main_end = out.find('</main>')
    ad_start = out.find('<div class="ad-slot">')
    prefix = out[:meta_end]
    middle = '\n' + html + '\n' + related_html + '\n</main>\n'
    suffix = out[main_end+7:ad_start] + out[ad_start:]

    result = prefix + middle + suffix

    filepath = os.path.join(OUTDIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f'  [OK] {filename}')

# ============================================================
# Article 2: Sheep or Ship — long/short vowels
# ============================================================
sheep_html = '''<p>英语里有五对长短元音，中文里没有这种区分。<span class="highlight">ship /ʃɪp/ 和 sheep /ʃiːp/ 只差一个音，意思从"船"变成"羊"</span>。本章聚焦最核心的三对长短元音，用对比练习帮你听出区别、说出标准。</p>

<h2>第一对：/ɪ/ vs /iː/ — 短"衣" vs 长"衣"</h2>
<p>发 /ɪ/ 时嘴巴微微张开，舌头位置略低，声音短促。发 /iː/ 时嘴巴向两边拉开，舌头抬高，声音拉长。<span class="highlight">关键区别：长短，不是松紧</span>。</p>

<div class="example"><div class="en">ship /ʃɪp/</div><div class="zh">船</div></div>
<div class="example"><div class="en">sheep /ʃiːp/</div><div class="zh">羊</div></div>
<div class="example"><div class="en">hit /hɪt/</div><div class="zh">打</div></div>
<div class="example"><div class="en">heat /hiːt/</div><div class="zh">热</div></div>
<div class="example"><div class="en">live /lɪv/</div><div class="zh">住</div></div>
<div class="example"><div class="en">leave /liːv/</div><div class="zh">离开</div></div>

<h2>第二对：/ʊ/ vs /uː/ — 短"呜" vs 长"呜"</h2>
<p>/ʊ/ 嘴巴微圆，短促。/uː/ 嘴巴更圆更撅，声音拉长。</p>
<div class="example"><div class="en">pull /pʊl/</div><div class="zh">拉</div></div>
<div class="example"><div class="en">pool /puːl/</div><div class="zh">游泳池</div></div>
<div class="example"><div class="en">full /fʊl/</div><div class="zh">满的</div></div>
<div class="example"><div class="en">fool /fuːl/</div><div class="zh">傻瓜</div></div>

<h2>第三对：/æ/ vs /ɑː/ — cat vs cart</h2>
<p>/æ/ 嘴巴张大，舌尖抵下齿，短促有力。/ɑː/ 嘴巴张更大，声音从喉咙深处拉长。</p>
<div class="example"><div class="en">cat /kæt/</div><div class="zh">猫</div></div>
<div class="example"><div class="en">cart /kɑːt/</div><div class="zh">手推车</div></div>
<div class="example"><div class="en">hat /hæt/</div><div class="zh">帽子</div></div>
<div class="example"><div class="en">heart /hɑːt/</div><div class="zh">心</div></div>

<h2>实战对比：逐对点读练习</h2>
<p>每对词只差一个元音长度。先点左边听短音，再点右边听长音，体会区别：</p>
<div class="example"><div class="en">ship</div><div class="zh">船（短 /ɪ/）</div></div>
<div class="example"><div class="en">sheep</div><div class="zh">羊（长 /iː/）</div></div>
<div class="example"><div class="en">pull</div><div class="zh">拉（短 /ʊ/）</div></div>
<div class="example"><div class="en">pool</div><div class="zh">游泳池（长 /uː/）</div></div>
<div class="example"><div class="en">cat</div><div class="zh">猫（短 /æ/）</div></div>
<div class="example"><div class="en">cart</div><div class="zh">手推车（长 /ɑː/）</div></div>

<h2>实战短句</h2>
<div class="example"><div class="en">I left my ship on the sheep farm.</div><div class="zh">我把船留在了养羊场。</div></div>
<div class="example"><div class="en">Don\'t pull me into the pool!</div><div class="zh">别把我拉进游泳池！</div></div>
<div class="example"><div class="en">The cat is sitting in the shopping cart.</div><div class="zh">猫坐在购物车里。</div></div>'''

write_article(
    'pronunciation-sheep-ship.html',
    'Sheep or Ship? — 长短元音 /iː/ vs /ɪ/ 你分得清吗 | 发音诊所 | 英语研习社',
    '英语长短元音对比练习：ship vs sheep、pull vs pool、cat vs cart。中文母语者专属纠音教程，音频点读对比。',
    'Sheep or Ship? — 长短元音 /iː/ vs /ɪ/ 你分得清吗',
    '<a href="index.html">首页</a> &raquo; <a href="pronunciation.html">发音诊所</a> &raquo; 长短元音：sheep vs ship',
    'pronunciation-sheep-ship.html',
    sheep_html,
    '<a href="pronunciation-th-sound.html">th音 think vs sink</a><a href="pronunciation-rl.html">r/l 不分</a><a href="pronunciation-vw.html">v/w 不分</a>'
)

# ============================================================
# Article 3: Rice or Lice — r/l confusion
# ============================================================
rl_html = '''<p>r/l 不分可能是中国英语学习者最经典的发音问题。中文里 r 和 l 不区分意义（"让"和"浪"你能分清，但英语里 rice 和 lice 是一个吃的、一个寄生虫）。<span class="highlight">核心区别：r 卷舌、l 舌尖顶上颚</span>。</p>

<h2>r 怎么发？</h2>
<p>嘴唇微微收圆，舌尖向上卷起靠近上颚但<strong>不碰到</strong>。声带振动，气流从舌头两侧和上方通过。</p>
<div class="example"><div class="en">red /red/</div><div class="zh">红色</div></div>
<div class="example"><div class="en">right /raɪt/</div><div class="zh">对的</div></div>
<div class="example"><div class="en">rice /raɪs/</div><div class="zh">米饭</div></div>
<div class="example"><div class="en">road /roʊd/</div><div class="zh">路</div></div>

<h2>l 怎么发？</h2>
<p>舌尖<strong>用力顶上齿龈</strong>（上排牙齿后面那块），声带振动，气流从舌头两侧出来。中文l和英语l位置一样，但英语l舌尖要更用力。</p>
<div class="example"><div class="en">led /led/</div><div class="zh">领导（过去式）</div></div>
<div class="example"><div class="en">light /laɪt/</div><div class="zh">光</div></div>
<div class="example"><div class="en">lice /laɪs/</div><div class="zh">虱子</div></div>
<div class="example"><div class="en">load /loʊd/</div><div class="zh">装载</div></div>

<h2>关键对比：r vs l</h2>
<p>逐一对比，点喇叭听区别：</p>
<div class="example"><div class="en">rice</div><div class="zh">米饭（r 卷舌不碰）</div></div>
<div class="example"><div class="en">lice</div><div class="zh">虱子（l 舌尖顶上去）</div></div>
<div class="example"><div class="en">right</div><div class="zh">对的（r 卷舌）</div></div>
<div class="example"><div class="en">light</div><div class="zh">光（l 顶上颚）</div></div>
<div class="example"><div class="en">rock</div><div class="zh">岩石（r）</div></div>
<div class="example"><div class="en">lock</div><div class="zh">锁（l）</div></div>
<div class="example"><div class="en">pray</div><div class="zh">祈祷（r）</div></div>
<div class="example"><div class="en">play</div><div class="zh">玩（l）</div></div>

<h2>最难的一对：词尾 -rl</h2>
<p>world、girl、pearl 这些词里 r 和 l 紧挨着，需要舌头快速从卷舌位切换到顶上颚位。这是终极挑战。</p>
<div class="example"><div class="en">world</div><div class="zh">世界</div></div>
<div class="example"><div class="en">girl</div><div class="zh">女孩</div></div>
<div class="example"><div class="en">pearl</div><div class="zh">珍珠</div></div>
<div class="example"><div class="en">girls around the world</div><div class="zh">全世界的女孩们</div></div>

<h2>实战短句</h2>
<div class="example"><div class="en">I really like the red light at the railway.</div><div class="zh">我真的喜欢铁路边的红灯。（4个r/l交替）</div></div>
<div class="example"><div class="en">The little girl is reading a lovely story.</div><div class="zh">小女孩在读一个可爱的故事。（多处l和r）</div></div>'''

write_article(
    'pronunciation-rl.html',
    'Rice or Lice? — 一劳永逸解决 r/l 不分 | 发音诊所 | 英语研习社',
    '英语r和l发音区别终极指南：rice vs lice、right vs light对比练习。核心口诀：r卷舌不碰、l舌尖顶上颚。中文母语者专属。',
    'Rice or Lice? — 一劳永逸解决 r/l 不分',
    '<a href="index.html">首页</a> &raquo; <a href="pronunciation.html">发音诊所</a> &raquo; r/l 不分：rice vs lice',
    'pronunciation-rl.html',
    rl_html,
    '<a href="pronunciation-th-sound.html">th音 think vs sink</a><a href="pronunciation-sheep-ship.html">长短元音</a><a href="pronunciation-vw.html">v/w 不分</a>'
)

# ============================================================
# Article 4: Very or Wary — v/w confusion
# ============================================================
vw_html = '''<p>中文里没有 /v/ 这个音，很多学习者用 /w/ 来代替。结果 very 说成了 wary，vest 说成了 west。<span class="highlight">核心区别：v上齿咬下唇、w双唇收圆</span>。</p>

<h2>v 怎么发？</h2>
<p>上排牙齿<strong>轻轻咬住下嘴唇内侧</strong>，气流从齿唇缝隙中挤出，声带振动。类似说"五"但用上牙咬住下唇。</p>
<div class="example"><div class="en">very /ˈveri/</div><div class="zh">非常</div></div>
<div class="example"><div class="en">vest /vest/</div><div class="zh">背心</div></div>
<div class="example"><div class="en">van /væn/</div><div class="zh">面包车</div></div>
<div class="example"><div class="en">voice /vɔɪs/</div><div class="zh">声音</div></div>

<h2>w 怎么发？</h2>
<p>双唇收圆撅起（像准备接吻），然后快速弹开到后面元音的位置。声带振动。<strong>牙齿不参与</strong>。</p>
<div class="example"><div class="en">wary /ˈweri/</div><div class="zh">谨慎的</div></div>
<div class="example"><div class="en">west /west/</div><div class="zh">西方</div></div>
<div class="example"><div class="en">wine /waɪn/</div><div class="zh">红酒</div></div>
<div class="example"><div class="en">wet /wet/</div><div class="zh">湿的</div></div>

<h2>关键对比：v vs w</h2>
<div class="example"><div class="en">very</div><div class="zh">非常（上牙咬下唇）</div></div>
<div class="example"><div class="en">wary</div><div class="zh">谨慎的（双唇收圆，牙不碰）</div></div>
<div class="example"><div class="en">vest</div><div class="zh">背心</div></div>
<div class="example"><div class="en">west</div><div class="zh">西方</div></div>
<div class="example"><div class="en">veil</div><div class="zh">面纱</div></div>
<div class="example"><div class="en">whale</div><div class="zh">鲸鱼</div></div>
<div class="example"><div class="en">vine</div><div class="zh">藤蔓</div></div>
<div class="example"><div class="en">wine</div><div class="zh">红酒</div></div>

<h2>特别注意：词首的 v</h2>
<p>很多中国学习者习惯把 video 说成 widio，visit 说成 wisit。纠正方法：<span class="highlight">说 v 开头的词之前，先有意识地把上牙放到下唇上</span>。</p>
<div class="example"><div class="en">video</div><div class="zh">视频（不是 widio）</div></div>
<div class="example"><div class="en">visit</div><div class="zh">拜访（不是 wisit）</div></div>
<div class="example"><div class="en">vegetable</div><div class="zh">蔬菜（不是 wegetable）</div></div>

<h2>实战短句</h2>
<div class="example"><div class="en">I was very wary of the wet weather in the west village.</div><div class="zh">我非常谨慎地对待西部村庄的潮湿天气。（v/w 五次交替）</div></div>
<div class="example"><div class="en">We visited several wonderful vineyards over the vacation.</div><div class="zh">我们假期参观了好几个很棒的葡萄园。（v/w 四次交替）</div></div>'''

write_article(
    'pronunciation-vw.html',
    'Very or Wary? — v / w 别再傻傻分不清 | 发音诊所 | 英语研习社',
    '英语v和w发音区别指南：very vs wary、vest vs west对比练习。核心口诀：v上牙咬下唇、w双唇收圆不碰牙。中文母语者专属。',
    'Very or Wary? — v / w 别再傻傻分不清',
    '<a href="index.html">首页</a> &raquo; <a href="pronunciation.html">发音诊所</a> &raquo; v/w 不分：very vs wary',
    'pronunciation-vw.html',
    vw_html,
    '<a href="pronunciation-th-sound.html">th音 think vs sink</a><a href="pronunciation-rl.html">r/l 不分</a><a href="pronunciation-nasal.html">鼻音 n vs ng</a>'
)

# ============================================================
# Article 5: Sun or Sung — nasal n vs ng
# ============================================================
nasal_html = '''<p>中文里有前后鼻音之分（"音"yīn vs "英"yīng），英语里同样有 /n/ 和 /ŋ/ 的区别。但英语的 /ŋ/ 比中文的后鼻音更"靠后"，<span class="highlight">舌头后部顶住软腭，让气流完全从鼻腔出来</span>。</p>

<h2>/n/ 怎么发？</h2>
<p>舌尖顶住上齿龈（跟 l 同位置），气流从鼻腔出来，声带振动。跟中文"那"的声母差不多。</p>
<div class="example"><div class="en">sun /sʌn/</div><div class="zh">太阳</div></div>
<div class="example"><div class="en">thin /θɪn/</div><div class="zh">薄的</div></div>
<div class="example"><div class="en">ban /bæn/</div><div class="zh">禁止</div></div>
<div class="example"><div class="en">ran /ræn/</div><div class="zh">跑（过去式）</div></div>

<h2>/ŋ/ 怎么发？</h2>
<p><strong>舌头后部拱起顶住软腭</strong>，舌尖不碰任何地方（这点跟 /n/ 完全不同）。气流完全从鼻腔出来，嘴巴微张。类似中文"英"的尾音，但要更靠后、更闷。</p>
<div class="example"><div class="en">sung /sʌŋ/</div><div class="zh">唱（过去分词）</div></div>
<div class="example"><div class="en">thing /θɪŋ/</div><div class="zh">东西</div></div>
<div class="example"><div class="en">bang /bæŋ/</div><div class="zh">砰</div></div>
<div class="example"><div class="en">rang /ræŋ/</div><div class="zh">响（过去式）</div></div>

<h2>关键对比：n vs ng</h2>
<div class="example"><div class="en">sun</div><div class="zh">太阳（舌尖顶上颚）</div></div>
<div class="example"><div class="en">sung</div><div class="zh">唱（舌头后部顶软腭，舌尖悬空）</div></div>
<div class="example"><div class="en">thin</div><div class="zh">薄的</div></div>
<div class="example"><div class="en">thing</div><div class="zh">东西</div></div>
<div class="example"><div class="en">ban</div><div class="zh">禁止</div></div>
<div class="example"><div class="en">bang</div><div class="zh">砰</div></div>
<div class="example"><div class="en">ran</div><div class="zh">跑</div></div>
<div class="example"><div class="en">rang</div><div class="zh">铃响了</div></div>

<h2>最容易搞混的三组</h2>
<p><strong>win / wing</strong> — "赢"和"翅膀"的意思完全不同。</p>
<div class="example"><div class="en">We\'re going to win.</div><div class="zh">我们会赢。</div></div>
<div class="example"><div class="en">a bird\'s wing</div><div class="zh">鸟的翅膀</div></div>

<p><strong>sin / sing</strong> — "罪"还是"唱歌"？别在教堂说错。</p>
<div class="example"><div class="en">That\'s a sin.</div><div class="zh">那是罪过。</div></div>
<div class="example"><div class="en">Let\'s sing a song.</div><div class="zh">我们唱首歌吧。</div></div>

<h2>一个自测技巧</h2>
<p>发 /ŋ/ 时，<strong>捏住鼻子应该发不出声</strong>（因为气流全从鼻腔走）。发 /n/ 时捏住鼻子，声音会变但还能发出来。你可以现在就试试：捏住鼻子说"sing"，如果还能出声，说明你的 /ŋ/ 发错了。</p>'''

write_article(
    'pronunciation-nasal.html',
    'Sun or Sung? — n 和 ng 的前后鼻音其实没那么难 | 发音诊所 | 英语研习社',
    '英语前后鼻音n和ng发音区别指南：sun vs sung、thin vs thing对比练习。含自测技巧：捏住鼻子发/ŋ/应该完全发不出声。',
    'Sun or Sung? — n 和 ng 的前后鼻音其实没那么难',
    '<a href="index.html">首页</a> &raquo; <a href="pronunciation.html">发音诊所</a> &raquo; 鼻音：sun vs sung',
    'pronunciation-nasal.html',
    nasal_html,
    '<a href="pronunciation-th-sound.html">th音 think vs sink</a><a href="pronunciation-vw.html">v/w 不分</a><a href="pronunciation-ed.html">词尾-ed发音</a>'
)

# ============================================================
# Article 6: Walked, Wanted, Played — -ed endings
# ============================================================
ed_html = '''<p>英语规则动词过去式加 -ed，看起来简单，但 -ed 的发音有三种：/t/、/d/、/ɪd/。<span class="highlight">很多人一律读成 /ɪd/，结果 walked 说成了 walk-ed，听起来像 walk-id</span>。看完这篇，你再也不会搞错。</p>

<h2>三种发音规则：看原形最后一个音</h2>
<table class="vocab-table">
<tr><th>-ed 发音</th><th>原形末尾音</th><th>例子</th><th>记忆口诀</th></tr>
<tr><td>/t/ 清辅音</td><td>清辅音：p, k, f, s, sh, ch, x</td><td>walked, hoped, laughed</td><td>清后清：原形是清辅音，-ed 也清</td></tr>
<tr><td>/d/ 浊辅音</td><td>浊辅音和元音：b, g, v, z, m, n, l, r, 元音</td><td>played, called, loved</td><td>浊后浊：原形是浊辅音或元音，-ed 也浊</td></tr>
<tr><td>/ɪd/ 额外音节</td><td>t 或 d 结尾</td><td>wanted, needed, started</td><td>t/d 后加 /ɪd/：原形已经是 t 或 d，必须加一个音节</td></tr>
</table>

<h2>第1组：/t/ — walked, talked, stopped</h2>
<p>原形以清辅音结尾，-ed 发清辅音 /t/。<strong>不要说 walk-ed，说 walkt</strong>。</p>
<div class="example"><div class="en">walked /wɔːkt/</div><div class="zh">走路（过去式）—— 不要说 walk-ed</div></div>
<div class="example"><div class="en">talked /tɔːkt/</div><div class="zh">说话（过去式）—— 不要说 talk-ed</div></div>
<div class="example"><div class="en">stopped /stɒpt/</div><div class="zh">停止（过去式）—— stoped 拼写也要双写 p</div></div>
<div class="example"><div class="en">laughed /læft/</div><div class="zh">笑（过去式）—— gh 发 /f/，所以 -ed 跟 /t/</div></div>

<h2>第2组：/d/ — played, called, loved</h2>
<p>原形以浊辅音或元音结尾，-ed 发浊辅音 /d/。</p>
<div class="example"><div class="en">played /pleɪd/</div><div class="zh">玩（过去式）—— 元音结尾，直接加 /d/</div></div>
<div class="example"><div class="en">called /kɔːld/</div><div class="zh">打电话（过去式）—— l 是浊辅音</div></div>
<div class="example"><div class="en">loved /lʌvd/</div><div class="zh">爱（过去式）—— v 是浊辅音，-ed 也浊</div></div>
<div class="example"><div class="en">opened /ˈəʊpənd/</div><div class="zh">打开（过去式）—— n 是浊辅音</div></div>

<h2>第3组：/ɪd/ — wanted, needed, started</h2>
<p>原形以 t 或 d 结尾时，-ed 必须发成额外音节 /ɪd/。<span class="highlight">这是唯一一种 -ed 增加一个音节的情况</span>。</p>
<div class="example"><div class="en">wanted /ˈwɒntɪd/</div><div class="zh">想要（过去式）—— 两个音节</div></div>
<div class="example"><div class="en">needed /ˈniːdɪd/</div><div class="zh">需要（过去式）—— 两个音节</div></div>
<div class="example"><div class="en">started /ˈstɑːtɪd/</div><div class="zh">开始（过去式）—— 两个音节</div></div>
<div class="example"><div class="en">decided /dɪˈsaɪdɪd/</div><div class="zh">决定（过去式）—— 三个音节</div></div>

<h2>对比练习：三组放一起听区别</h2>
<div class="example"><div class="en">walked</div><div class="zh">走路（/t/，清）</div></div>
<div class="example"><div class="en">played</div><div class="zh">玩（/d/，浊）</div></div>
<div class="example"><div class="en">wanted</div><div class="zh">想要（/ɪd/，额外音节）</div></div>

<h2>实战短句</h2>
<div class="example"><div class="en">I walked to the store, called my mom, and waited for the bus.</div><div class="zh">我走到商店，给妈妈打了电话，然后等公交。（三个 -ed 三种发音）</div></div>
<div class="example"><div class="en">She loved the movie, but her friend hated it.</div><div class="zh">她喜欢那部电影，但她朋友讨厌它。（loved /d/, hated /ɪd/）</div></div>
<div class="example"><div class="en">He stopped, looked, and listened.</div><div class="zh">他停下来，看了看，听了听。（三个 -ed 都发 /t/）</div></div>

<h2>口诀总结</h2>
<div class="example"><div class="en">清后 /t/，浊后 /d/，t/d 后面加 /ɪd/。</div><div class="zh">记住这10个字，-ed发音永不出错。</div></div>'''

write_article(
    'pronunciation-ed.html',
    'Walked, Wanted, Played — 词尾 -ed 到底发哪个音？ | 发音诊所 | 英语研习社',
    '英语规则动词过去式词尾-ed三种发音规则完整指南：/t/、/d/、/ɪd/。含对比练习和口诀：清后t、浊后d、t/d后面加ɪd。',
    'Walked, Wanted, Played — 词尾 -ed 到底发哪个音？',
    '<a href="index.html">首页</a> &raquo; <a href="pronunciation.html">发音诊所</a> &raquo; 词尾 -ed：walked vs wanted vs played',
    'pronunciation-ed.html',
    ed_html,
    '<a href="pronunciation-th-sound.html">th音 think vs sink</a><a href="pronunciation-nasal.html">鼻音 n vs ng</a><a href="pronunciation-sheep-ship.html">长短元音</a>'
)

print('\nAll 5 articles generated.')
