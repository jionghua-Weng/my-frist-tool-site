#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate 5 new daily-*.html articles from template and article content data."""

import sys, os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TEMPLATE = "daily-coffee.html"
OUTDIR = ".."

ARTICLES = [
    {
        "file": "daily-small-talk.html",
        "title_tag": 'Can\'t Beat the Weather — 天气是最好的开场白：聚会闲聊全攻略 | 英语研习社',
        "desc": "掌握英语Small Talk的核心技巧，从天气、周末、工作等万能话题到实战对话，让你的社交英语不再冷场。学会优雅开场、自然过渡、从容退场。",
        "h1": 'Can\'t Beat the Weather — 天气是最好的开场白：聚会闲聊全攻略',
        "breadcrumb": '<a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 聚会闲聊 Small Talk',
        "html": """<p>Small talk 是英语社交的润滑剂。老外见面不直接谈正事，先聊天气、周末、旅行——这叫"破冰"。很多人怕冷场，其实掌握几个万能话题就够了。</p>

<h2>Small Talk 四法则</h2>
<p>1. <strong>从当下环境出发</strong>——派对聊音乐，咖啡店聊咖啡，话题就在你身边。</p>
<p>2. <strong>问开放性问题</strong>——别用 Yes/No 能把天聊死的问法。<span class="highlight">What do you enjoy about...? 比 Do you like...? 好十倍</span>。</p>
<p>3. <strong>给信息，不只索取</strong>——别人问"How was your weekend?"，别回"Good"然后沉默。加一句"I finally checked out that new ramen place"，对话就流动起来了。</p>
<p>4. <strong>避开三雷区</strong>——政治、宗教、工资。闲聊不是辩论赛。</p>

<h2>五大万能开场</h2>
<h3>天气——永不翻车</h3>
<div class="example"><div class="en">Beautiful day, isn't it? / Can you believe this rain? It was sunny all week and now this.</div><div class="zh">天气真好，对吧？/ 你敢信这雨？一周大晴天结果今天下成这样。</div></div>

<h3>周末——最自然的过渡</h3>
<div class="example"><div class="en">How was your weekend? Did you get up to anything fun? / Doing anything exciting this weekend?</div><div class="zh">周末过得怎么样？有什么好玩的吗？/ 这周末有什么安排？</div></div>

<h3>工作/学习——安全区</h3>
<div class="example"><div class="en">How long have you been working here? What do you enjoy most about it? / What got you into that field?</div><div class="zh">你在这工作多久了？最喜欢哪个部分？/ 是什么让你进入这个领域的？</div></div>

<h3>吃喝——最容易展开</h3>
<div class="example"><div class="en">Have you tried that new sushi place on Main Street? I've been meaning to check it out. / I'm a bit of a coffee snob — any recommendations around here?</div><div class="zh">你试过主街那家新开的寿司店吗？我一直想去。/ 我对咖啡有点挑——这附近有推荐吗？</div></div>

<h3>旅行——永远不会冷</h3>
<div class="example"><div class="en">Have you traveled anywhere interesting recently? / If you could hop on a plane tomorrow, where would you go?</div><div class="zh">最近去过什么好玩的地方？/ 明天就能跳上飞机的话，你会去哪？</div></div>

<h2>实战对话：派对上第一次见面</h2>
<p>掌握这套对话，下一次派对你不会再站墙角看手机。</p>
<div class="dialogue">
<div class="line"><span class="speaker">Alex：</span>Hey, I don't think we've met. I'm Alex — a friend of Sarah's.</div>
<div class="line"><span class="speaker">Jamie：</span>Nice to meet you! I'm Jamie. I work with Sarah. How do you know her?</div>
<div class="line"><span class="speaker">Alex：</span>College roommates, freshman year. Quite the experience.</div>
<div class="line"><span class="speaker">Jamie：</span>Oh I bet. So are you here just for the party, or do you live nearby?</div>
<div class="line"><span class="speaker">Alex：</span>I live about 20 minutes away. Just moved here last year. Still discovering the area.</div>
<div class="line"><span class="speaker">Jamie：</span>Nice! If you need restaurant recs, I've been here forever. I know all the hidden spots.</div>
<div class="line"><span class="speaker">Alex：</span>That'd be amazing. What's your go-to place?</div>
</div>

<h2>优雅退场</h2>
<p>聊得差不多了，怎么自然地结束对话？</p>
<div class="example"><div class="en">It was great chatting with you! I'm gonna grab another drink — let's catch up later.</div><div class="zh">聊得很开心！我去拿杯喝的，回头聊。</div></div>
<div class="example"><div class="en">I don't want to monopolize your evening. It was really nice meeting you!</div><div class="zh">不想占你一整晚——很高兴认识你！</div></div>

<h2>救场过渡句</h2>
<p>对话尴尬了？用这几句接上：</p>
<div class="example"><div class="en">That reminds me... / Speaking of which, have you heard about...? / Anyway, I was going to ask you...</div><div class="zh">这让我想起来…… / 说到这个，你听说……了吗？ / 对了，我正想问你……</div></div>""",
        "related": '<a href="daily-coffee.html">用英文点咖啡</a><a href="daily-restaurant.html">餐厅英语全流程</a><a href="patterns-the-thing-is.html">The thing is 过渡句</a><a href="patterns-polite.html">委婉沟通三个句型</a>'
    },
    {
        "file": "daily-hair-salon.html",
        "title_tag": '别让发型毁了你：理发店英语 How to Talk to Your Hair Stylist | 英语研习社',
        "desc": "理发店英语全攻略：从预约、描述发型、剪发术语到付款小费，一篇搞定。不再靠比划跟发型师沟通，男士女士都适用。",
        "h1": '别让发型毁了你：理发店英语 How to Talk to Your Hair Stylist',
        "breadcrumb": '<a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 理发店英语',
        "html": """<p>理发是出国最容易翻车的场景之一。你跟发型师说"剪短一点"，他可能理解为推成板寸。本章帮你把理发相关的英文一次性搞清楚——从预约到付款，不靠比划。</p>

<h2>预约：电话或到店第一句</h2>
<div class="example"><div class="en">Hi, I'd like to book a haircut. Do you have any openings this weekend? / I'm looking to get a trim and maybe some layers. Is there a stylist available this afternoon?</div><div class="zh">你好，我想预约剪发。这周末有空位吗？/ 我想修一下，可能打点层次。今天下午有发型师吗？</div></div>

<h2>核心词汇表：理发店必懂的术语</h2>
<table class="vocab-table">
<tr><th>中文</th><th>英文</th><th>说明</th></tr>
<tr><td>修剪（少量）</td><td>trim</td><td>只修发尾，不动长度</td></tr>
<tr><td>剪短</td><td>cut / chop</td><td>chop 更口语，"咔嚓掉"</td></tr>
<tr><td>打薄</td><td>thin out / texturize</td><td>发量多时用</td></tr>
<tr><td>层次</td><td>layers</td><td>长短交错，有动感</td></tr>
<tr><td>刘海</td><td>bangs (美) / fringe (英)</td><td>额头前面那撮</td></tr>
<tr><td>鬓角</td><td>sideburns</td><td>耳朵前面那块</td></tr>
<tr><td>发梢分叉</td><td>split ends</td><td>发尾开叉</td></tr>
<tr><td>烫发</td><td>perm</td><td>化学药水烫卷</td></tr>
<tr><td>染发</td><td>color / dye</td><td>color 比 dye 更常用</td></tr>
<tr><td>挑染</td><td>highlights / balayage</td><td>balayage 是法式刷染</td></tr>
<tr><td>渐变（男士）</td><td>fade</td><td>两边渐变短发</td></tr>
</table>

<h2>怎么描述你想要的发型</h2>
<div class="example"><div class="en">I just want a trim — take off about an inch, and clean up the ends.</div><div class="zh">我只想修一下——剪掉大概一英寸，把发尾修整齐。</div></div>
<div class="example"><div class="en">Could you take a little off the sides and leave the top longer?</div><div class="zh">两边打薄一点，上面留着。</div></div>
<div class="example"><div class="en">I want to keep the length overall, but add some layers for movement.</div><div class="zh">我想保留整体长度，加点层次，让头发有动感。</div></div>

<h2>实战对话：女士剪发</h2>
<div class="dialogue">
<div class="line"><span class="speaker">Stylist：</span>So what are we thinking today?</div>
<div class="line"><span class="speaker">你：</span>I want to keep the length, but add some layers around the face. Maybe take off an inch at the ends — they're pretty dead.</div>
<div class="line"><span class="speaker">Stylist：</span>Got it. What about the bangs? Do you want to keep them?</div>
<div class="line"><span class="speaker">你：</span>Just a trim on the bangs — keep them above the eyebrows but not too short.</div>
<div class="line"><span class="speaker">Stylist：</span>And styling-wise, do you usually air-dry or blow-dry?</div>
<div class="line"><span class="speaker">你：</span>Mostly air-dry, so I need something low-maintenance.</div>
<div class="line"><span class="speaker">Stylist：</span>Perfect. Let's do long layers with face-framing pieces. I'll thin out the back a bit so it doesn't feel heavy.</div>
</div>

<h2>男士理发实用句</h2>
<div class="example"><div class="en">I'll take a number 3 on the sides, and scissor cut on top. Keep the top about two inches long.</div><div class="zh">两边用3号推子，上面用剪刀修。上面留大概两英寸。</div></div>
<div class="example"><div class="en">Can you do a low fade on the sides and leave the top textured?</div><div class="zh">两边做个低位渐变，上面保留纹理感。</div></div>
<div class="example"><div class="en">Just clean up the neckline and around the ears, and a slight trim on top.</div><div class="zh">修一下脖子边和耳朵周围，上面稍微剪短一点就行。</div></div>

<h2>万一不满意，怎么补救</h2>
<div class="example"><div class="en">Actually, could you take a bit more off the sides? They feel a little uneven. / The bangs are a little shorter than I expected — could we blend them in a bit more?</div><div class="zh">其实两边能再打薄一点吗？感觉有点不对称。/ 刘海比我预期的短了点——能再融合自然一点吗？</div></div>

<h2>付款和给小费</h2>
<div class="example"><div class="en">How much do I owe you? / Do you take card or cash? / Keep the change. / Is gratuity included?</div><div class="zh">多少钱？/ 刷卡还是现金？/ 不用找了。/ 服务费含了吗？</div></div>
<p>美国理发小费一般是总价的 15%–20%，加拿大类似。英国和澳洲通常不需要额外给小费，但可以说一句 "Keep the change"。</p>""",
        "related": '<a href="daily-shopping.html">购物英语全覆盖</a><a href="daily-restaurant.html">餐厅英语全流程</a><a href="patterns-polite.html">委婉沟通三个句型</a><a href="patterns-wondering-if.html">I was wondering if 句型</a>'
    },
    {
        "file": "daily-renting.html",
        "title_tag": 'How Much Is Rent? 租房英语：从看房到签约 | 英语研习社',
        "desc": "海外租房英语全流程指南：找房联系、看房提问10句、合同关键条款、报修对话。留学生和海外工作必看，租房不踩坑。",
        "h1": 'How Much Is Rent? 租房英语：从看房到签约',
        "breadcrumb": '<a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 租房英语',
        "html": """<p>留学生和海外工作的人，第一个要过的语言关不是课堂英语，是租房英语。看房时听不懂房东说什么，签合同时漏掉关键条款，报修时描述不清问题——每一步都可能踩坑。搭配<a href="patterns-wondering-if.html">I was wondering if 句型</a>，让你的租房沟通更自然。</p>

<h2>找房阶段：第一轮联系</h2>
<div class="example"><div class="en">Hi, I'm interested in the apartment listed on Zillow. Is it still available? / I was wondering if you could tell me a bit more about the place — what's the neighborhood like? / When would be a good time to schedule a viewing?</div><div class="zh">你好，我对 Zillow 上挂的那套公寓感兴趣，还在租吗？/ 想了解一下这个房子的更多信息——周边环境怎么样？/ 什么时候方便约看房？</div></div>

<h2>租房核心词汇</h2>
<table class="vocab-table">
<tr><th>中文</th><th>英文</th><th>说明</th></tr>
<tr><td>押金</td><td>security deposit</td><td>通常等于一个月租金</td></tr>
<tr><td>水电煤气</td><td>utilities</td><td>水电气总称</td></tr>
<tr><td>包含水电</td><td>utilities included</td><td>房租含水电</td></tr>
<tr><td>租约</td><td>lease</td><td>有法律效力的租房合同</td></tr>
<tr><td>房东</td><td>landlord / landlady</td><td>男/女房东</td></tr>
<tr><td>室友</td><td>roommate / flatmate</td><td>flatmate 更偏英式</td></tr>
<tr><td>带/不带家具</td><td>furnished / unfurnished</td><td>看房必问</td></tr>
<tr><td>提前解约</td><td>break the lease</td><td>中途退租</td></tr>
<tr><td>转租</td><td>sublet</td><td>把房子转租给别人</td></tr>
<tr><td>物业费</td><td>HOA fee (美) / service charge (英)</td><td>公寓楼的额外费用</td></tr>
</table>

<h2>看房时必问的10个问题</h2>
<p>拿着这个清单去看房，一个关键问题都不会漏：</p>
<div class="example"><div class="en">1. Are utilities included, or are they separate? / 2. How much is the security deposit, and when is it due? / 3. What's the lease term — is it month-to-month or a fixed year? / 4. Is there a penalty for breaking the lease early? / 5. Are pets allowed? Is there a pet deposit? / 6. How's the water pressure? Can I test the shower? / 7. What's the heating / AC situation? / 8. How do you handle repairs? Is there a maintenance number? / 9. Is there laundry in the building? / 10. How's the noise level — can you hear the neighbors?</div><div class="zh">1. 水电含不含？2. 押金多少、什么时候交？3. 租期是月付还是年签？4. 提前解约有罚款吗？5. 能养宠物吗？有宠物押金吗？6. 水压怎么样？能试淋浴吗？7. 暖气和空调怎么配置？8. 维修怎么报？有维修电话吗？9. 楼里有洗衣房吗？10. 隔音怎么样——能听到邻居噪音吗？</div></div>

<h2>实战对话：看房</h2>
<div class="dialogue">
<div class="line"><span class="speaker">你：</span>Hi, thanks for showing me the place. It looks great in the photos, but I had a few questions.</div>
<div class="line"><span class="speaker">房东：</span>Of course, ask away.</div>
<div class="line"><span class="speaker">你：</span>First — does the rent include any utilities? Water, gas, internet?</div>
<div class="line"><span class="speaker">房东：</span>Water and trash are included. Electricity and internet are separate. Usually they run about $80 to $120 a month combined.</div>
<div class="line"><span class="speaker">你：</span>Got it. And what about the lease — is it a one-year minimum?</div>
<div class="line"><span class="speaker">房东：</span>Yes, it's a 12-month lease. After that it goes month-to-month automatically.</div>
<div class="line"><span class="speaker">你：</span>One more — how do you handle maintenance? If the sink leaks or the heater breaks down, who do I call?</div>
<div class="line"><span class="speaker">房东：</span>You can text me directly for anything urgent. For non-urgent stuff, just submit a request through the tenant portal and my handyman usually comes within 48 hours.</div>
</div>

<h2>签合同要看的关键条款</h2>
<div class="example"><div class="en">Make sure you understand: the move-in date and lease end date / how much notice you need to give before moving out (usually 30 or 60 days) / what happens if you need to break the lease / the late fee policy if rent is overdue / whether subletting is allowed</div><div class="zh">一定看清楚：入住日期和租约到期日 / 退租需要提前多久通知（一般是30或60天）/ 提前解约的违约责任 / 租金逾期交多少滞纳金 / 能不能转租</div></div>

<h2>报修：东西坏了怎么说</h2>
<div class="example"><div class="en">Hi, the sink in the kitchen is leaking. Could you send someone to take a look? / The heater isn't working — it's been blowing cold air since last night. Is there an emergency maintenance number? / The toilet keeps running after you flush it. Not an emergency, but I wanted to let you know.</div><div class="zh">厨房水槽漏水，能派人来看一下吗？/ 暖气不制热了——从昨晚开始一直吹冷风。有紧急维修电话吗？/ 马桶冲完后一直流水。不是什么急事，就跟你知会一声。</div></div>""",
        "related": '<a href="daily-hotel.html">酒店入住英语</a><a href="daily-transport.html">交通出行英语</a><a href="patterns-wondering-if.html">I was wondering if 句型</a><a href="vocabulary-used-to.html">used to 用法辨析</a>'
    },
    {
        "file": "daily-taxi.html",
        "title_tag": '"Where to, sir?" — 打车/叫车英语全攻略 | 英语研习社',
        "desc": "打车和网约车英语全覆盖：扬招对话、Uber实战、改路线、纠错说法、付款表达，一篇让你去哪都能顺利到达。",
        "h1": '"Where to, sir?" — 打车/叫车英语，目的地、改路线、付款全搞定',
        "breadcrumb": '<a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 打车英语',
        "html": """<p>不管是在纽约街头扬招一辆 Yellow Cab，还是用 Uber 在伦敦叫车，打车的英语对话其实高度固定。<span class="highlight">掌握这些模板，你永远不会跟司机鸡同鸭讲</span>。</p>

<h2>扬招 / 上车第一句</h2>
<div class="example"><div class="en">Taxi! / Are you free? / Can you take me to [place]? / I'm going to the airport, Terminal 3. / Do you know how to get to this address?</div><div class="zh">出租车！/ 空车吗？/ 能送我去[地点]吗？/ 我去机场T3航站楼。/ 你知道这个地址怎么走吗？</div></div>

<h2>用车/网约车常用词</h2>
<table class="vocab-table">
<tr><th>中文</th><th>英文</th><th>说明</th></tr>
<tr><td>目的地/下车点</td><td>destination / drop-off</td><td>drop-off 是下车位置</td></tr>
<tr><td>上车点</td><td>pickup / pick-up location</td><td>司机来接你的地方</td></tr>
<tr><td>拼车</td><td>carpool / shared ride</td><td>Uber Pool 之类，更便宜</td></tr>
<tr><td>计价器</td><td>meter</td><td>打表计费</td></tr>
<tr><td>一口价</td><td>flat rate</td><td>固定价格不跳表</td></tr>
<tr><td>小费</td><td>tip / gratuity</td><td>网约车可在App内给</td></tr>
<tr><td>后备箱</td><td>trunk (美) / boot (英)</td><td>放大件行李用</td></tr>
<tr><td>安全带</td><td>seatbelt</td><td>上车系好</td></tr>
</table>

<h2>途中可能用到的句子</h2>
<div class="example"><div class="en">Could you turn up the AC a bit? It's pretty warm back here.</div><div class="zh">能开大点空调吗？后面挺热的。</div></div>
<div class="example"><div class="en">Actually, could we take the highway instead? I think it's faster this time of day.</div><div class="zh">其实能走高速吗？这个点我觉得高速更快。</div></div>
<div class="example"><div class="en">I'm in a bit of a rush — is there a shortcut you could take?</div><div class="zh">我有点赶时间——有没有近道可以走？</div></div>
<div class="example"><div class="en">You can just drop me off here, at the corner. That's perfect.</div><div class="zh">你就把我放这个拐角就行，正好。</div></div>
<div class="example"><div class="en">Could you pop the trunk? I've got a suitcase.</div><div class="zh">能开下后备箱吗？我有个行李箱。</div></div>

<h2>实战对话：Uber 去机场</h2>
<div class="dialogue">
<div class="line"><span class="speaker">司机：</span>Hi, are you [your name]? Heading to the airport?</div>
<div class="line"><span class="speaker">你：</span>Yes, that's me. Terminal 3, please — international departures.</div>
<div class="line"><span class="speaker">司机：</span>Got it. About 35 minutes depending on traffic. You in a hurry?</div>
<div class="line"><span class="speaker">你：</span>I've got about two hours before my flight, so no rush. But I'd prefer the highway if it's not too much trouble.</div>
<div class="line"><span class="speaker">司机：</span>No problem. The 405 should be moving okay this time of day. Need any music or should I keep it quiet?</div>
<div class="line"><span class="speaker">你：</span>Whatever you prefer — I'm good either way.</div>
<div class="line"><span class="speaker">司机：</span>Here we are — Terminal 3. Your gate should be upstairs. Do you need the trunk?</div>
<div class="line"><span class="speaker">你：</span>Yeah, I've got a checked bag. Thanks so much for the ride. I'll tip you in the app.</div>
<div class="line"><span class="speaker">司机：</span>Appreciate it. Have a safe flight!</div>
</div>

<h2>付款环节</h2>
<div class="example"><div class="en">How much is the fare? / Can I pay by card? / Keep the change. / Could I get a receipt, please? / Can you break a fifty?</div><div class="zh">多少钱？/ 能刷卡吗？/ 不用找了。/ 能给我张发票吗？/ 五十块找得开吗？</div></div>

<h2>出了差错怎么办</h2>
<p>走错路了？下车位置不对？直接说，别不好意思：</p>
<div class="example"><div class="en">I think we might be going the wrong way — my map shows a different route.</div><div class="zh">我觉得我们可能走错了——我地图上显示的是另外一条路。</div></div>
<div class="example"><div class="en">Excuse me, I said 5th Avenue, not 5th Street. Could you make a U-turn?</div><div class="zh">不好意思，我说的是第五大道，不是第五街。能掉个头吗？</div></div>
<div class="example"><div class="en">Actually, this isn't the right drop-off. My app shows the pickup is across the street.</div><div class="zh">这个下车点不对，我的App显示上车点在马路对面。</div></div>""",
        "related": '<a href="daily-airport.html">机场必备英语</a><a href="daily-transport.html">交通出行英语</a><a href="daily-hotel.html">酒店入住英语</a><a href="patterns-wondering-if.html">I was wondering if 句型</a>'
    },
    {
        "file": "daily-banking.html",
        "title_tag": "I'd Like to Open an Account — 银行英语：开户、换汇、转账 | 英语研习社",
        "desc": "海外银行英语一站搞定：开户对话、换汇汇率、国际汇款SWIFT、挂失补卡全流程。刚到英语国家必看的金融英语指南。",
        "h1": "I'd Like to Open an Account — 银行开户、换汇、转账实用英语",
        "breadcrumb": '<a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 银行英语',
        "html": """<p>刚到英语国家的第二件事（第一件是租房），就是去银行开户。银行术语本身就够复杂了，换成英文更容易懵。<span class="highlight">本章覆盖开户、换汇、转账、挂失四个最核心场景</span>，让你走进银行心里有底。</p>

<h2>开户：走进银行第一段对话</h2>
<div class="example"><div class="en">Hi, I'd like to open a bank account. What types of accounts do you offer? / Is there a minimum balance requirement? / Are there any monthly fees? / What documents do I need to bring?</div><div class="zh">你好，我想开个银行账户。你们有哪几种账户？/ 有最低余额要求吗？/ 有月费吗？/ 我需要带什么证件？</div></div>

<h2>银行核心词汇</h2>
<table class="vocab-table">
<tr><th>中文</th><th>英文</th><th>说明</th></tr>
<tr><td>活期账户</td><td>checking account (美) / current account (英)</td><td>日常支付用</td></tr>
<tr><td>储蓄账户</td><td>savings account</td><td>存钱吃利息</td></tr>
<tr><td>借记卡</td><td>debit card</td><td>直接扣账户余额</td></tr>
<tr><td>信用卡</td><td>credit card</td><td>先消费后还款</td></tr>
<tr><td>余额</td><td>balance</td><td>账户里有多少钱</td></tr>
<tr><td>存款</td><td>deposit</td><td>把钱存进去</td></tr>
<tr><td>取款</td><td>withdraw / withdrawal</td><td>把钱取出来</td></tr>
<tr><td>转账</td><td>transfer / wire transfer</td><td>wire 是电汇</td></tr>
<tr><td>货币兑换</td><td>currency exchange</td><td>换汇</td></tr>
<tr><td>汇率</td><td>exchange rate</td><td>两种货币的兑换比率</td></tr>
<tr><td>手续费</td><td>fee / service charge</td><td>银行收的各种费用</td></tr>
<tr><td>透支</td><td>overdraft</td><td>账户余额变负数</td></tr>
<tr><td>挂失</td><td>report a lost / stolen card</td><td>卡丢了第一时间说这句</td></tr>
<tr><td>对账单</td><td>statement / bank statement</td><td>每月账单</td></tr>
</table>

<h2>实战对话：开户</h2>
<div class="dialogue">
<div class="line"><span class="speaker">你：</span>Hi, I'd like to open an account. I just moved here for work.</div>
<div class="line"><span class="speaker">Banker：</span>Welcome! So you'll want a checking account for everyday use. Do you want to open a savings account as well?</div>
<div class="line"><span class="speaker">你：</span>Just the checking account for now. What are the requirements?</div>
<div class="line"><span class="speaker">Banker：</span>A minimum opening deposit of $25, and we need two forms of ID — passport and proof of address, like a utility bill or lease.</div>
<div class="line"><span class="speaker">你：</span>I've got both right here. Are there any monthly maintenance fees I should know about?</div>
<div class="line"><span class="speaker">Banker：</span>There's a $12 monthly fee, but it's waived if you keep a minimum daily balance of $1,500 or set up direct deposit with your employer.</div>
<div class="line"><span class="speaker">你：</span>I can do the direct deposit. How long does it take to get the debit card?</div>
<div class="line"><span class="speaker">Banker：</span>The card will arrive by mail in 7 to 10 business days. But I can give you a temporary card you can use today.</div>
</div>

<h2>换汇：我需要换点外币</h2>
<div class="example"><div class="en">I'd like to exchange some currency. What's the exchange rate for US dollars to euros today? / Could I exchange ¥10,000 RMB for US dollars, please? / Are there any fees for currency exchange? / I'd like to withdraw some cash from my account — could I get that in pounds?</div><div class="zh">我想换点外币。今天美元兑欧元汇率是多少？/ 能帮我把一万人民币换成美元吗？/ 换汇有手续费吗？/ 我想从账户取点现金——能取英镑吗？</div></div>

<h2>转账：国内转账 vs 国际汇款</h2>
<div class="example"><div class="en">I need to make a transfer to another account. / I'd like to send a wire transfer overseas. What information do I need from the recipient? / How long does an international wire usually take? / What's the SWIFT / IBAN code I need to use? / Is there a limit on how much I can transfer per day?</div><div class="zh">我要转一笔钱到另一个账户。/ 我想做一笔国际电汇。需要收款人提供哪些信息？/ 国际汇款一般多久到账？/ 我需要用哪个SWIFT码/IBAN号？/ 每天转账有限额吗？</div></div>

<h2>挂失：卡丢了第一时间要做什么</h2>
<div class="example"><div class="en">Hi, I need to report a lost card. I think I left my debit card at a restaurant last night. / My card has been stolen — I need to freeze my account immediately. / Can you issue a replacement card? How long will it take? / Will I be liable for any charges made after I lost the card?</div><div class="zh">你好，我要挂失一张卡。我昨晚好像把借记卡落在一家餐厅了。/ 我的卡被偷了——请立刻冻结我的账户。/ 能补发一张新卡吗？多久能到？/ 卡丢失后产生的消费我要负责吗？</div></div>

<h2>其他常用句</h2>
<div class="example"><div class="en">What's my current balance? / Could I get a printed statement for the last three months? / I'd like to set up automatic bill pay for my rent. / Is there an ATM nearby? Do you charge a fee for using other banks' ATMs? / Can I increase my daily withdrawal limit?</div><div class="zh">我现在余额多少？/ 能帮我打印最近三个月的对账单吗？/ 我想设置房租自动扣款。/ 附近有ATM吗？用别的银行ATM你们收手续费吗？/ 能提高我的每日取现额度吗？</div></div>""",
        "related": '<a href="daily-renting.html">租房英语全流程</a><a href="daily-shopping.html">购物英语全覆盖</a><a href="daily-interview.html">面试英语必备</a><a href="patterns-wondering-if.html">I was wondering if 句型</a>'
    },
]


def generate():
    # Read template — look in parent dir (yingyu-site/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    tpl_path = os.path.join(parent_dir, TEMPLATE)
    if not os.path.exists(tpl_path):
        print(f"ERROR: Template {tpl_path} not found")
        sys.exit(1)

    with open(tpl_path, "r", encoding="utf-8") as f:
        tpl = f.read()

    base_dir = parent_dir

    for a in ARTICLES:
        out = tpl

        # Replace title tag
        out = out.replace(
            "用英文点咖啡：不只是\"Coffee, please\" — 场景口语 | 英语研习社",
            a["title_tag"]
        )

        # Replace meta description
        # Find and replace the description meta
        old_desc_start = out.find('<meta name="description" content="')
        old_desc_end = out.find('">', old_desc_start) + 2
        old_desc = out[old_desc_start:old_desc_end]
        new_desc = '<meta name="description" content="' + a["desc"] + '">'
        out = out.replace(old_desc, new_desc, 1)

        # Replace og:title
        old_og_title = "用英文点咖啡：不只是&quot;Coffee, please&quot; — 场景口语 | 英语研习社"
        new_og_title = a["title_tag"].replace('"', '&quot;')
        out = out.replace(old_og_title, new_og_title, 1)

        # Replace og:description
        old_og_desc = "从星巴克到精品咖啡馆，一篇搞懂用英文点咖啡的全部用语。卡布奇诺、拿铁、半糖、去冰——所有你需要的表达都在这里。"
        out = out.replace(old_og_desc, a["desc"], 1)

        # Replace twitter:title
        old_tw_title = "用英文点咖啡：不只是&quot;Coffee, please&quot; — 场景口语 | 英语研习社"
        out = out.replace(old_tw_title, new_og_title, 1)

        # Replace twitter:description
        old_tw_desc = "从星巴克到精品咖啡馆，一篇搞懂用英文点咖啡的全部用语。卡布奇诺、拿铁、半糖、去冰——所有你需要的表达都在这里。"
        out = out.replace(old_tw_desc, a["desc"], 1)

        # Replace og:url
        out = out.replace(
            'content="https://easyeng.club/daily-coffee.html"',
            'content="https://easyeng.club/' + a["file"] + '"'
        )

        # Replace breadcrumb
        old_bread = '<div class="breadcrumb"><a href="index.html">首页</a> &raquo; <a href="daily.html">场景口语</a> &raquo; 用英文点咖啡：不只是"Coffee, please"</div>'
        new_bread = '<div class="breadcrumb">' + a["breadcrumb"] + '</div>'
        out = out.replace(old_bread, new_bread, 1)

        # Replace h1
        old_h1 = '<h1>用英文点咖啡：不只是"Coffee, please"</h1>'
        new_h1 = '<h1>' + a["h1"] + '</h1>'
        out = out.replace(old_h1, new_h1, 1)

        # Replace article content (between <h1>...</h1>+meta and <div class="related">)
        # Find <div class="related">
        rel_start = out.find('<div class="related">')
        # Find the </main> after meta
        main_start = out.find('<main class="article">')
        content_start = out.find('</div>', out.find('class="meta"')) + 6  # After meta div

        # Build new content
        meta_end = out.find('</div>', out.find('class="meta"')) + 6
        prefix = out[:meta_end]
        suffix = out[rel_start:]

        new_content = prefix + "\n" + a["html"] + "\n"
        new_content += '<div class="related"><h3>相关文章</h3>' + a["related"] + '</div>\n'
        new_content += suffix[suffix.find('</main>'):]

        # Actually, let me reconstruct more carefully
        out = out[:meta_end] + "\n" + a["html"] + "\n"
        out += '<div class="related"><h3>相关文章</h3>' + a["related"] + '</div>\n</main>'

        # Add everything after </main> from template
        suffix = tpl[tpl.find('</main>') + 7:]
        out += suffix

        # Write
        filepath = os.path.join(base_dir, a["file"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"  [OK] {a['file']}")


if __name__ == "__main__":
    generate()
