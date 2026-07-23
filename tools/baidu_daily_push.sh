#!/bin/bash
# 百度SEO每日推送 — 每天推10条URL
# 由 Claude Code cron 定时触发

URL_FILE="/d/Claude Code/yingyu-site/sitemap_urls_www.txt"
PROGRESS_FILE="/d/Claude Code/yingyu-site/tools/baidu_push_progress.txt"
TOKEN="u9T7InagdVXyx6TE"
API="http://data.zz.baidu.com/urls?site=https://www.easyeng.club&token=$TOKEN"

# 读进度
if [ ! -f "$PROGRESS_FILE" ]; then
    echo "0" > "$PROGRESS_FILE"
fi
START=$(cat "$PROGRESS_FILE")
TOTAL=$(wc -l < "$URL_FILE")

# 检查是否已完成
if [ "$START" -ge "$TOTAL" ]; then
    echo "全部完成: $START/$TOTAL 条已推送"
    exit 0
fi

# 取下一批10条
END=$((START + 10))
if [ "$END" -gt "$TOTAL" ]; then
    END=$TOTAL
fi

# 提取URL
URLS=$(sed -n "$((START + 1)),${END}p" "$URL_FILE")
echo "$URLS" | curl -s -H 'Content-Type:text/plain' --data-binary @- "$API"

# 更新进度
echo "$END" > "$PROGRESS_FILE"
echo "进度: $END/$TOTAL"
