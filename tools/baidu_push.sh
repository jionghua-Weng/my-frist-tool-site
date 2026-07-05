#!/bin/bash
# 百度SEO URL推送脚本 — 每天10条，逐步推送全站sitemap
# 调用方式: ./baidu_push.sh [--init] [--dry-run]

SITEMAP="/www/wwwroot/easyeng.club/sitemap.xml"
STATE_FILE="/root/baidu_pushed.txt"
LOG_FILE="/root/baidu_push.log"
TOKEN="u9T7InagdVXyx6TE"
SITE="easyeng.club"
DAILY_LIMIT=10

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 提取sitemap中所有URL
extract_urls() {
    grep -oP '(?<=<loc>)[^<]+' "$SITEMAP"
}

# 初始化状态文件（记录已推送URL）
if [ "$1" = "--init" ] && [ ! -f "$STATE_FILE" ]; then
    log "初始化状态文件"
    extract_urls > /dev/null  # 仅验证sitemap可读
    touch "$STATE_FILE"
    log "状态文件创建完毕: $STATE_FILE"
    exit 0
fi

if [ ! -f "$STATE_FILE" ]; then
    log "状态文件不存在，先运行 --init"
    exit 1
fi

# 获取待推送URL（尚未推送的）
ALL_URLS=$(extract_urls)
PUSHED=$(cat "$STATE_FILE" 2>/dev/null)

# 取前N条未推送的URL
COUNT=0
BATCH=""
while IFS= read -r url; do
    if [ $COUNT -ge $DAILY_LIMIT ]; then
        break
    fi
    if ! grep -qFx "$url" "$STATE_FILE" 2>/dev/null; then
        BATCH="$BATCH$url"$'\n'
        COUNT=$((COUNT + 1))
    fi
done <<< "$ALL_URLS"

if [ $COUNT -eq 0 ]; then
    log "全部URL已推送完毕"
    exit 0
fi

BATCH=$(echo "$BATCH" | sed '/^$/d')

log "本次推送 $COUNT 条URL"

if [ "$1" = "--dry-run" ]; then
    log "[DRY-RUN] 将推送以下URL:"
    echo "$BATCH" | while read -r url; do
        echo "  $url"
    done
    exit 0
fi

# 调用百度API
RESPONSE=$(curl -s -X POST "http://data.zz.baidu.com/urls?site=$SITE&token=$TOKEN" \
    -H "Content-Type: text/plain" \
    -d "$BATCH" 2>&1)

log "API响应: $RESPONSE"

# 解析响应，记录成功的URL
SUCCESS=$(echo "$RESPONSE" | grep -oP '(?<="success":)\d+' || echo "0")
if [ "$SUCCESS" -gt 0 ]; then
    echo "$BATCH" >> "$STATE_FILE"
    log "成功推送 $SUCCESS 条，累计 $(wc -l < "$STATE_FILE") 条"
else
    log "推送失败: $RESPONSE"
fi
