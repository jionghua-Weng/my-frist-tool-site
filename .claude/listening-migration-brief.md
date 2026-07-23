# 听力模块搬迁任务

## 来源
LetMeEnglish.com 的听力训练页面：https://letmeenglish.com/zh-hans/listening/

## 目标
把整个听力模块（课程内容+音频+交互）复制到英语研习社，作为发音/听力子模块。

## 已完成的分析

### 课程数量
- 初级听力：53 篇
- 中级听力：39 篇
- 合计：92 篇

### 音频架构
每课两种音频：
1. 逐句 MP3（听写练习用）：`/wp-content/uploads/{YYYY}/{MM}/{标题}_{序号}.mp3`，每句 ~8KB
2. 全文 MP3：`/wp-content/uploads/{YYYY}/{MM}/{标题}_full.mp3`，~560KB

总音频量：~2000+ 碎片文件 + 92 全文文件 ≈ 60-70MB

### 前端架构
- 插件：`lmd-typing-exercise`（WordPress 插件）
- JS：~200 行 jQuery，负责：逐题切换、调速播放(0.5x-1.5x)、输入比对、键盘快捷键
- 数据：每课的 `ddeExercises` JS 数组，含 audio_url + correct_answer

## 已抓取的页面
- 列表页：`D:\Claude Code\lme_listening.html`
- 示例课（A Snowy Day）：`D:\Claude Code\lme_snowy_day.html`
- 插件 JS：`D:\Claude Code\lme_script.js`

## 执行计划
1. 写 Python 爬虫 → 抓取 92 课数据（音频 URL + 正确文本 + 双语翻译）
2. 下载全部 MP3 到 `audio/listening/`
3. 搭建 HTML 模板（仿 yingyu-site 风格，原生 JS 不依赖 jQuery）
4. 批量生成 92 个课程页面 + 1 个列表主页

## 目标结构
```
yingyu-site/
├── listening.html              ← 听力主页
├── listening/                  ← 课程页面（或直接放根目录）
│   ├── a-snowy-day.html
│   └── ...
├── audio/listening/            ← MP3 文件
│   ├── a-snowy-day/
│   │   ├── 1.mp3 ... 22.mp3
│   │   └── full.mp3
│   └── ...
```
